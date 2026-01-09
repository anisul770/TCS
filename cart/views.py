from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,ListModelMixin
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from cart.serializers import CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer
from cart.models import Cart,CartItem
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet,ListModelMixin):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
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
    
    