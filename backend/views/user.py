from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from backend.models import MyUser, Family
from backend.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
        _Resumo_
        Classe que define as operações de CRUD para o modelo MyUser, que representa um usuário do sistema.

        _Requisições_
        - list (GET): Retorna apenas o usuário autenticado. Requer autenticação.
        - retrieve (GET): Retorna um usuário específico. Requer autenticação.
        - create (POST): Quando passado um argumento de busca chamado 'search_term' e um 'family_id' fixo, este método faz uma busca por usuários que não pertencem a família especificada, baseado no argumento de busca. Quando não passado um argumento de busca chamado 'search_term', este método cria um novo usuário. Como o usuário que está criando sua conta não estará autenticado, este método não requer autenticação para ser acessado.
        - update (PUT): Atualiza um usuário específico. Requer autenticação.
        - partial_update (PATCH): Atualiza parcialmente um usuário específico. Requer autenticação.
        - destroy (DELETE): Deleta um usuário específico. Requer autenticação.
    """
    
    lookup_field = 'user_id'
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return MyUser.objects.filter(email = self.request.user)
        return MyUser.objects.none()
    
    def create(self, request):
        data = request.data
        input_search = data.get('search_term')
        if input_search:
            family_id = data.get('family_id')
            family = Family.objects.get(family_id=family_id)
            queryset = MyUser.objects.filter(
                Q(email__icontains=input_search) |
                Q(first_name__icontains=input_search) |
                Q(last_name__icontains=input_search)
            ).exclude(email__in=family.family_members)
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)