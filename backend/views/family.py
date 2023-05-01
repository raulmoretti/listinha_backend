from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from backend.models import Family
from backend.serializers import FamilySerializer

class FamilyViewSet(ModelViewSet):
    """
        _Resumo_
        Classe que define as operações de CRUD para o modelo Family, que representa uma família de usuários. Uma família é um grupo de usuários que compartilham um carrinho de compra, assim como as respectivas ordens de compra deste carrinho.
        
        _Requisições_
        - list (GET): Retorna todas as famílias em que o usuário autenticado pertence. Requer autenticação.
        - retrieve (GET): Retorna uma família específica em que o usuário autenticado pertence. Requer autenticação.
        - create (POST): Cria uma nova família. Requer autenticação.
        - update (PUT): Atualiza uma família específica. Requer autenticação.
        - partial_update (PATCH): Atualiza parcialmente uma família específica. Requer autenticação.
        - destroy (DELETE): Deleta uma família específica. Requer autenticação.
    
    """
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Family.objects.filter(family_members__contains=[str(user)])
        else:
            return Family.objects.none()
                
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        instance = super().create(request, *args, **kwargs)
        return Response({'family_id': instance.data['family_id']}, status=status.HTTP_201_CREATED)