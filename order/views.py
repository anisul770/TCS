from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from order.serializers import OrderSerializer,OrderItemSerializer,CreateOrderSerializer
from order.models import Order,OrderItem
# Create your views here.

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer