from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,ListModelMixin
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from cart.serializers import CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer
from cart.models import Cart,CartItem

# Create your views here.

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet,ListModelMixin):
    serializer_class = CartSerializer
    
    def perform_create(self, serializer):
        try:
            serializer.save(user = self.request.user)
        except IntegrityError:
            raise ValidationError({'details':'You already have a cart'})
        
    def get_queryset(self):
        return Cart.objects.prefetch_related('items').prefetch_related('items__service').all()
    
class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AddCartItemSerializer
        if self.action == 'update':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs.get('cart_pk')}
    
    def get_queryset(self):
        return CartItem.objects.select_related('service').filter(cart_id = self.kwargs.get('cart_pk'))
    
    