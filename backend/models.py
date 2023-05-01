import uuid
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Cria e salva um usuário com o email, nome e sobrenome e senha fornecidos
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Cria e salva um super usuário com o email, nome e sobrenome e senha fornecidos
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    
    def get_by_natural_key(self, email):
        return self.get(email=email)
    

class MyUser(AbstractBaseUser, PermissionsMixin):
    
    """ Adiciona o campo email """
    email = models.EmailField(max_length=255, unique=True, primary_key=True)
    
    """ Campos adicionais """
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)
    families = ArrayField(models.TextField(), blank=True, default=list)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = MyUserManager()
    
    
    """ Configura o campo USERNAME_FIELD como email ao invés de username, e adiciona o campo REQUIRED_FIELDS que configura os campos obrigatórios """
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    
class Family(models.Model):
    family_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    family_name = models.CharField(max_length=255, blank=False, null=False)
    family_members = ArrayField(models.TextField(), blank=True, default=list)
    family_owner = models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    has_cart = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if str(self.family_owner) not in self.family_members:
            self.family_members.append(self.family_owner)
        if str(self.family_id) not in self.family_owner.families:
            self.family_owner.families.append(self.family_id)
            self.family_owner.save()
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        users = MyUser.objects.filter(families__contains=[str(self.family_id)])
        for user in users:
            user.families.remove(str(self.family_id))
            user.save()
        super().delete(*args, **kwargs)
            
    def add_member(self, user):
        self.family_members.append(user)

    def remove_member(self, user):
        self.family_members.remove(user)
   
        
class Product(models.Model):
    # Campos
    product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    product_owner = models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length=255, blank=False, null=False)
    product_brand = models.CharField(max_length=255, blank=True, null=True)
    product_type = models.CharField(max_length=255, blank=True, null=True)
    favorite = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    

class SMCart(models.Model):
    # Campos
    cart_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    cart_owner = models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    cart_family = models.ForeignKey('Family', on_delete=models.CASCADE, null=True)
    cart_comments = models.TextField(blank=True, null=True)
    cart_orders = ArrayField(models.TextField(), blank=True, default=list)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Quando um carrinho é criado, mudar o campo has_cart da família correspondente para True
    def save(self, *args, **kwargs):
        family = Family.objects.get(family_id=self.cart_family.family_id)
        family.has_cart = True
        family.save()
        super().save(*args, **kwargs)
        
           
class Order(models.Model):
    # Campos
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    order_owner = models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    order_product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    order_cart = models.ForeignKey('SMCart', on_delete=models.CASCADE, null=True)
    order_quantity = models.IntegerField()
    order_comment = models.TextField(null=True, blank=True)
    
    # Método que, sempre que uma ordem for criada, seu id seja adicionado ao array cart_orders do modelo SMcart correspondente caso esse id ainda não esteja lá
    def save(self, *args, **kwargs):
        cart = SMCart.objects.get(cart_id=str(self.order_cart.cart_id))
        if str(self.order_id) not in cart.cart_orders:
            cart.cart_orders.append(str(self.order_id))
            cart.save()
        super().save(*args, **kwargs)
        
    # O mesmo para o método delete
    def delete(self, *args, **kwargs):
        cart = SMCart.objects.get(cart_id=str(self.order_cart.cart_id))
        cart.cart_orders.remove(str(self.order_id))
        cart.save()
        super().delete(*args, **kwargs)
    
    
class FamilyRequest(models.Model):
    # Opções
    REQUEST_STATUS = (
        ('P', 'Pendente'),
        ('A', 'Aceito'),
        ('R', 'Recusado'),
    )
    
    # Campos
    request_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    request_new_member = models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True, related_name='request_new_member')
    request_owner = models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)
    request_family = models.ForeignKey('Family', on_delete=models.CASCADE, null=True)
    request_status = models.CharField(max_length=1, choices=REQUEST_STATUS, default='P')
    created_at = models.DateTimeField(default=timezone.now)
    request_message = models.TextField(null=True, blank=True)