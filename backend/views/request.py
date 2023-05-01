import json
from django.shortcuts import render, get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from backend.models import MyUser, Family, FamilyRequest
from backend.serializers import FamilyRequestSerializer, FamilyRequestListSerializer

class FamilyRequestViewSet(ModelViewSet):
    """
        _Resumo_
        Classe que define as operações de CRUD para o modelo FamilyRequest, que representa uma solicitação de entrada em uma família de um usuário para outro usuário.
        
        _Requisições_
        - list (GET): Retorna todas as solicitações de entrada em famílias feitas ao usuário autenticado. Requer autenticação.
        - retrieve (GET): Retorna uma solicitação de entrada em família específica feitas ao usuário autenticado. Requer autenticação.
        - create (POST): Cria uma nova solicitação de entrada em família. Requer autenticação.
        - update (PUT): Atualiza uma solicitação de entrada em família específica. Requer autenticação.
        - partial_update (PATCH): Atualiza parcialmente uma solicitação de entrada em família específica. Requer autenticação.
        - destroy (DELETE): Deleta uma solicitação de entrada em família específica. Requer autenticação.
    
    """
    queryset = FamilyRequest.objects.all()
    serializer_class = FamilyRequestSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return FamilyRequest.objects.filter(request_new_member=user)
        else:
            return FamilyRequest.objects.none()
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FamilyRequestListSerializer
        return FamilyRequestSerializer
            
    
    def create(self, request, *args, **kwargs):
        data = request.data
        user = self.request.user.email
        new_dict = {}

        request_new_member = get_object_or_404(MyUser, email=data.get('request_new_member'))
        request_family = get_object_or_404(Family, family_id=data.get('request_family'))
        request_owner = get_object_or_404(MyUser, email=user)
        new_dict['request_new_member'] = str(request_new_member)
        new_dict['request_message'] = data.get('request_message')
        new_dict['request_family'] = str(request_family.family_id)
        new_dict['request_owner'] = str(request_owner)

        serializer = FamilyRequestSerializer(data=new_dict)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Muda o status da requisição para 'accepted' e adicionar o email do novo membro na lista de membros da família quando o usuário aceitar a requisição
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data.get('request_status') == 'A':
            instance.request_status = 'A'
            instance.save()
            
            new_member = get_object_or_404(MyUser, email=instance.request_new_member.email)
            family = get_object_or_404(Family, family_id=instance.request_family.family_id)

            family.family_members.append(new_member.email)
            family.save()
            new_member.families.append(family.family_id)
            new_member.save()
            return Response(status=status.HTTP_200_OK)
        elif request.data.get('request_status') == 'R':
            instance.request_status = 'R'
            instance.save()
            return Response(status=status.HTTP_200_OK)