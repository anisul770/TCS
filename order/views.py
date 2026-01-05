from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from order.serializers import OrderSerializer,OrderItemSerializer
from order.models import Order,OrderItem
# Create your views here.

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()