from django.contrib import admin
from django.contrib.auth.models import Group

from .models import MyUser, Family, Product, Order, SMCart, FamilyRequest


class MyUserAdmin(admin.ModelAdmin):
    
    # Campos que serão exibidos na listagem
    list_display = ('email', 'first_name', 'last_name', 'password', 'families','is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
    list_filter = ('email', 'first_name', 'last_name', 'password', 'families', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
    
    # Campos que serão exibidos no formulário de edição
    fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'password', 'families','is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
        }),
    )
    # Campos que serão exibidos no formulário de criação
    add_fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'password', 'confirm_password', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()  
    

class FamilyAdmin(admin.ModelAdmin):
    list_display = ('family_name', 'family_owner', 'family_members', 'has_cart','created_at', 'is_active', 'family_id')
    list_filter = ('family_name', 'family_owner', 'family_members', 'has_cart','created_at', 'is_active', 'family_id')
    fieldsets = (
        (None, {
            'fields': ('family_name', 'family_owner', 'family_members', 'has_cart', 'created_at', 'is_active')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('family_name', 'family_owner', 'family_members', 'has_cart', 'created_at', 'is_active')
        }),
    )    


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_owner', 'product_name', 'product_brand', 'product_type', 'favorite', 'image', 'product_id')
    list_filter = ('product_owner', 'product_name', 'product_brand', 'product_type', 'favorite', 'image', 'product_id')
    fieldsets = (
        (None, {
            'fields': ('product_owner', 'product_name', 'product_brand', 'product_type', 'favorite', 'image')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('product_owner', 'product_name', 'product_brand', 'product_type', 'favorite', 'image')
        }),
    )


class SMCartAdmin(admin.ModelAdmin):
    list_display = ('cart_owner', 'cart_family', 'cart_comments', 'cart_orders','created_at', 'cart_id')
    list_filter = ('cart_owner', 'cart_family', 'cart_comments', 'cart_orders','created_at', 'cart_id')
    fieldsets = (
        (None, {
            'fields': ('cart_owner', 'cart_family', 'cart_comments', 'cart_orders', 'created_at')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('cart_owner', 'cart_family', 'cart_comments', 'cart_orders', 'created_at')
        }),
    )
         

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_owner','order_product', 'order_cart', 'order_quantity', 'order_comment', 'order_id')
    list_filter = ('order_owner','order_product', 'order_cart', 'order_quantity', 'order_comment', 'order_id')
    fieldsets = (
        (None, {
            'fields':('order_owner','order_product', 'order_cart', 'order_quantity', 'order_comment')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('order_owner','order_product', 'order_cart', 'order_quantity', 'order_comment')
        }),
    )
    
    
class FamilyResquestAdmin(admin.ModelAdmin):
    list_display = ('request_owner', 'request_new_member','request_family', 'request_status', 'request_message','request_id', 'created_at')
    list_filter = ('request_owner', 'request_new_member','request_family', 'request_status', 'request_message','request_id', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('request_owner', 'request_new_member','request_family', 'request_status', 'request_message', 'created_at')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('request_owner', 'request_new_member','request_family', 'request_status', 'request_message', 'created_at')
        }),
    )


# Registrando os modelos no admin
admin.site.unregister(Group)
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SMCart, SMCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(FamilyRequest, FamilyResquestAdmin)