from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from order.serializers import OrderSerializer,OrderItemSerializer,CreateOrderSerializer,UpdateOrderSerializer,EmptySerializer
from order.models import Order,OrderItem
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from order.services import OrderService
# Create your views here.

class OrderViewSet(ModelViewSet):
    http_method_names = ['get','post','delete','patch','head','options']
    
    @action(detail=True,methods=['post'])
    def cancel(self,request,pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order,user=request.user)
        return Response({'status' : 'Order Canceled'})
    
    @action(detail=True,methods=['patch'])
    def update_status(self,request,pk=None):
        order = self.get_object()
        serializer = UpdateOrderSerializer(order,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status':f"Order status updated to {request.data['status']}"})
    
    def get_permissions(self):
        if self.action in ['destroy','update_status']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'cancel':
            return EmptySerializer
        if self.action == 'create':
            return CreateOrderSerializer
        elif self.action in ['update_status','partial_update']:
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):   
        if getattr(self,'swagger_fake_view',False):
            return super().get_serializer_context()
        return {'user_id' : self.request.user.id,'user' : self.request.user}
    
    def get_queryset(self):
        if getattr(self,'swagger_fake_view',False):
            return Order.objects.none()
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('user').prefetch_related('items__service').all()
        return Order.objects.prefetch_related('user').prefetch_related('items__service').filter(user= self.request.user)
    