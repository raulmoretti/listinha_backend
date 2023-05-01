from django.contrib.auth import authenticate

from rest_framework import exceptions
from rest_framework.serializers import ModelSerializer, CharField, ValidationError, ImageField
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from backend.models import MyUser, Family, Product, Order, SMCart, FamilyRequest

      
class FamilyListSerializer(ModelSerializer):
    class Meta:
        model = Family
        fields = ('family_id', 'family_name', 'family_owner', 'family_members', 'created_at', 'is_active')
 
        
class UserSerializer(ModelSerializer):
    confirm_password = CharField(max_length=128, write_only=True)
    
    class Meta:
        model = MyUser
        fields = (
            'email', 'first_name', 'last_name', 'password', 'confirm_password', 'date_joined', 'last_login', 'families', 'user_id'
        )
        read_only_fields = ('date_joined', 'last_login', 'families', 'user_id')
        depth = 2
            
    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError("As senhas não conferem. Tente novamente")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        instance = MyUser.objects.create_user(**validated_data)
        return instance
    
    # Método para pegar o campo families que é uma lista de UUIDs e retornar uma lista com todos os campos correspondentes a esses UUIDs da tabela Family
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['families'] = FamilyListSerializer(Family.objects.filter(family_id__in=representation['families']), many=True).data
        return representation

      
class FamilySerializer(ModelSerializer): 
    class Meta:
        model = Family
        fields = '__all__'
        read_only_fields = ('created_at', 'is_active', 'family_members', 'family_owner')
    
    # Adicionar a lista family_members caso ela não exista, para que possa ser passada ao método save() do modelo Family, que irá adicionar o usuário logado à lista.
    def create(self, validated_data):
        if 'family_members' not in validated_data:
            validated_data.update({'family_members': []})
        validated_data.update({'family_owner': self.context['request'].user})
        instance = Family.objects.create(**validated_data)
        return instance
        
       
class UserListSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name', 'user_id')
        

class ProductSerializer(ModelSerializer):
    product_owner = UserListSerializer
    image = ImageField(required=False, allow_null=True, allow_empty_file=True)
    class Meta:
        model = Product
        fields = '__all__'
        

class SMCartSerializer(ModelSerializer):
    class Meta:
        model = SMCart
        fields = '__all__'
        read_only_fields = ('created_at',)
        

class OrderSerializer(ModelSerializer):
    order_product = ProductSerializer
    order_cart = SMCartSerializer
    class Meta:
        model = Order
        fields = '__all__'
        depth = 1
        
        
class OrderCreateSerializer(ModelSerializer):
    order_product = ProductSerializer
    order_cart = SMCartSerializer
    class Meta:
        model = Order
        fields = '__all__'
        
        
class FamilyRequestSerializer(ModelSerializer):
    request_owner = UserListSerializer
    request_new_member = UserListSerializer
    request_family = FamilySerializer
    class Meta:
        model = FamilyRequest
        fields = '__all__'
 
 
class FamilyRequestListSerializer(ModelSerializer):
    request_owner = UserListSerializer
    request_new_member = UserListSerializer
    request_family = FamilySerializer
    class Meta:
        model = FamilyRequest
        fields = '__all__'
        depth = 1
 
 
class MyTokenObtainSerializer(TokenObtainSerializer):
    username_field = MyUser.USERNAME_FIELD
    # O resto da classe é igual ao TokenObtainPairSerializer
    def validate(self, attrs):
        self.user = authenticate(self.context['request'], **{
            self.username_field: attrs[self.username_field],
            'password': attrs['password']
        })
        
        if not self.user:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        
        if not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        
        return {}
    
    
class MyTokenObtainPairSerializer(MyTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data