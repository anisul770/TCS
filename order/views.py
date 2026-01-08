from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from order.serializers import OrderSerializer,OrderItemSerializer,CreateOrderSerializer,UpdateOrderSerializer
from order.models import Order,OrderItem
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from order.services import OrderService
# Create your views here.

class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post','delete','patch','head','options']
    
    @action(detail=True,methods=['post'],permission_classes=[IsAuthenticated])
    def cancel(self,request,pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order,user=request.user)
        return Response({'status' : 'Order Canceled'})
        
    def get_permissions(self):
        if self.action in ['destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        elif self.action == 'partial_update':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id' : self.request.user.id,'user':self.request.user}
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items').prefetch_related('items__service').all()
        return Order.objects.prefetch_related('items').prefetch_related('items__service').filter(user= self.request.user)