from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,ListModelMixin
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from cart.serializers import CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer
from cart.models import Cart,CartItem
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet,ListModelMixin):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Create new Cart by the User',
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Show The cart of the user'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete the cart by the owner or admin'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Show cart details'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        try:
            serializer.save(user = self.request.user)
        except IntegrityError:
            raise ValidationError({'details':'You already have a cart'})
        
    def get_queryset(self):
        if getattr(self,'swagger_fake_view',False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items').prefetch_related('items__service').filter(user=self.request.user)
    
class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    
    @swagger_auto_schema(
        operation_summary='Show all the cart items'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Add new item to the cart'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Show item details'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Edit quantity of the items'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Edit cart item'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Remove item from the cart'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AddCartItemSerializer
        if self.action == 'update':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        if getattr(self,'swagger_fake_view',False):
            return super().get_serializer_context()
        return {'cart_id':self.kwargs.get('cart_pk')}
    
    def get_queryset(self):
        if getattr(self,'swagger_fake_view',False):
            return CartItem.objects.none()
        return CartItem.objects.select_related('service').filter(cart_id = self.kwargs.get('cart_pk'))
    
    