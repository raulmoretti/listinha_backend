import os, json
from django.db.models import Q
from django.conf import settings

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from backend.models import Product
from backend.serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    """
        _Resumo_
        Classe que define as operações de CRUD para o modelo Product, que representa um produto cadastrado por um usuário, que ficará disponível apenas para ele.
        
        _Requisições_
        - list (GET): Retorna todos os produtos cadastrados pelo usuário autenticado. Requer autenticação.
        - retrieve (GET): Retorna um produto específico cadastrado pelo usuário autenticado. Requer autenticação.
        - create (POST): Quando passado no body da requisição um argumento de busca chamad 'search_term', este método faz uma busca por produtos cadastrados pelo usuário autenticado, baseado no argumento de busca. Quando não passado um argumento de busca chamado 'search_term', este método cria um novo produto. Requer autenticação.
        - update (PUT): Atualiza um produto específico cadastrado pelo usuário autenticado. Requer autenticação.
        - partial_update (PATCH): Atualiza parcialmente um produto específico cadastrado pelo usuário autenticado. Requer autenticação.
        - destroy (DELETE): Deleta um produto específico cadastrado pelo usuário autenticado. Requer autenticação.
    
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(product_owner=user) 
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    # Quando um produto é deletado, pegue o nome do arquivo de imagem, procura ele no diretório images e delete esse arquivo de la
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.image:
            image = instance.image
            path = os.path.join(settings.MEDIA_ROOT, image.name)
            if os.path.isfile(path):
                os.remove(path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        user = self.request.user
        data = request.data
        input_search = data.get('search_term')
        if input_search:
            queryset = Product.objects.filter(
                Q(product_owner=user) & (
                Q(product_name__icontains=input_search) |
                Q(product_brand__icontains=input_search) |
                Q(product_type__icontains=input_search)
            ))
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data)
        else:

            new_dict = {}
            new_dict['product_name'] = data.get('product_name')
            new_dict['product_owner'] = str(user.email)
            if data.get('product_brand') != '':
                new_dict['product_brand'] = data.get('product_brand')
            if data.get('product_type') != '':
                 new_dict['product_type'] = data.get('product_type')
            if data.get('image') != '':
                new_dict['image'] = data.get('image')
            

            # data['product_owner'] = str(user.email)

            serializer = ProductSerializer(data=new_dict)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # Sobrescreve o método responsável por editar (PATCH) uma instancia do modelo Product, para que, quando o usuário insira uma nova imagem, a imagem antiga seja deletada do diretório images e a nova imagem seja salva no diretório images. Porém, caso o usuário não insira uma nova imagem, e o campo de imagem venha vazio, cria um novo dicionário com os dados do request, exceto o campo de imagem, e salva no banco de dados.
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        if data.get('image') != '' or data.get('image') != None or data.get('image') != 'undefined' or data.get('image') != 'null':
            if instance.image:
                image = instance.image
                path = os.path.join(settings.MEDIA_ROOT, image.name)
                if os.path.isfile(path):
                    os.remove(path)
            serializer = ProductSerializer(instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            new_dict = {}
            new_dict['product_name'] = data.get('product_name')
            if data.get('product_brand') != '':
                new_dict['product_brand'] = data.get('product_brand')
            if data.get('product_type') != '':
                 new_dict['product_type'] = data.get('product_type')
            serializer = ProductSerializer(instance, data=new_dict, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)