from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from backend.models import Order, SMCart, Family
from backend.serializers import OrderSerializer, OrderCreateSerializer

class OrderViewSet(ModelViewSet):
    """_Resumo_
        Classe que define as operações de CRUD para o modelo Order, que representa uma ordem de compra de um produto que o usuário possui cadastrado em seu email para um carrinho de compras de uma família em que esse usuário pertence.

        _Requisições_
        - list (GET): Retorna todas as ordens de compra feitas por membros de famílias em que o usuário autenticado pertence. Requer autenticação.
        - retrieve (GET): Retorna uma ordem de compra específica feita por membros de famílias em que o usuário autenticado pertence. Requer autenticação.
        - create (POST): Cria uma nova ordem de compra. Requer autenticação.
        - update (PUT): Atualiza uma ordem de compra específica. Requer autenticação.
        - partial_update (PATCH): Atualiza parcialmente uma ordem de compra específica. Requer autenticação.
        - destroy (DELETE): Deleta uma ordem de compra específica. Requer autenticação.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
      
    def get_queryset(self):
        user = self.request.user
        user_families = Family.objects.filter(family_members__contains=[str(user)])
        families_carts = SMCart.objects.filter(cart_family__in=user_families)
        cart_orders = Order.objects.filter(order_cart__in=families_carts)
        return cart_orders

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    # Sobrescreve o método create para que o campo order_owner seja definido como o usuário logado
    def create(self, request, *args, **kwargs):
        data = request.data

        user = self.request.user.email
        new_dict = {}

        order_owner = user
        order_cart = data.get('order_cart')
        order_comment = data.get('order_comment')
        order_quantity = data.get('order_quantity')
        order_product = data.get('order_product')

        new_dict['order_owner'] = str(order_owner)
        new_dict['order_cart'] = str(order_cart)
        new_dict['order_comment'] = order_comment
        new_dict['order_quantity'] = order_quantity
        new_dict['order_product'] = str(order_product)

        serializer = OrderCreateSerializer(data=new_dict)
 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)