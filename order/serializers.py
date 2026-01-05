from rest_framework import serializers
from order.models import Order,OrderItem
from cart.serializers import SimpleServiceSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleServiceSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','price','total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True)
    class Meta:
        model = Order
        fields = ['id','user','status','total_price','created_at','updated_at','items']
        read_only_fields = ['total_price','created_at','updated_at']
        