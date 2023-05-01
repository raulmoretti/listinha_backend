from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from backend.models import SMCart, Family, MyUser, Order
from backend.serializers import SMCartSerializer

class SMCartViewSet(ModelViewSet):
    """
        _Resumo_
        Classe que define as operações de CRUD para o modelo SMCart (Supermarket Cart), que representa um carrinho de compras de uma família. Um carrinho de compras é um conjunto de ordens de compra, que são feitas por usuários pertencentes a família que o carrinho pertence. Um familia só deverá ter um carrinho de compras por vez. A idéia é, quando uma família é criada, qualquer membro dessa família pode criar o carrinho de compras, e então permitir que todos os membros possam incluir ordens de compra a esse carrinho. Quando a pessoa da família que vai ao supermercado fazer as compras termina de fazer as compras, ela pode encerrar o carrinho de compras, e então esse carrinho junto as ordens de compra relacionadas a ele são deletados, permitindo que outro carrinho seja criado pela família.
        
        _Atributos_
        - list (GET): Lista todos os carrinhos de compras de todas as famílias que o usuário autenticado pertence.
        - retrieve (GET): Retorna um carrinho de compras específico de uma família específica que o usuário autenticado pertence.
        - create (POST): Cria um novo carrinho de compras para uma família específica do usuário autenticado. Requer autenticação.
        - update (PUT): Atualiza um carrinho de compras específico de uma família específica do usuário autenticado. Requer autenticação.
        - partial_update (PATCH): Atualiza parcialmente um carrinho de compras específico de uma família específica do usuário autenticado. Requer autenticação.
        - destroy (DELETE): Deleta um carrinho de compras específico de uma família específica do usuário autenticado. Requer autenticação.
    
    """
    
    lookup_field = 'cart_family'
    queryset = SMCart.objects.all()
    serializer_class = SMCartSerializer

    def get_queryset(self):
        user = self.request.user
        user_families = Family.objects.filter(family_members__contains=[str(user)])
        cart_families = SMCart.objects.filter(cart_family__in=user_families)
        return cart_families

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
        
    # Sobrescreve o método create para que o campo cart_owner seja definido como o usuário logado
    def create(self, request, *args, **kwargs):
        data = request.data

        user = self.request.user.email
        new_dict = {}

        cart_owner = get_object_or_404(MyUser, email=user)
        cart_family = get_object_or_404(Family, family_id=data.get('cart_family'))
        cart_comments = data.get('cart_comments')

        new_dict['cart_owner'] = str(cart_owner)
        new_dict['cart_family'] = str(cart_family.family_id)
        new_dict['cart_comments'] = cart_comments

        serializer = SMCartSerializer(data=new_dict)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Sobrescreve o método delete para que, antes do carrinho ser deletado, muda o campo has_cart da familia correspondente para False e delete todas as orders relacionadas a esse carrinho, se houverem, e depois deleta o carrinho
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        orders = Order.objects.filter(order_cart=instance.cart_id)
        if orders:
            for order in orders:
                order.delete()
        family = Family.objects.get(family_id=instance.cart_family.family_id)
        family.has_cart = False
        family.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)