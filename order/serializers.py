from rest_framework import serializers
from order.models import Order,OrderItem
from cart.serializers import SimpleServiceSerializer
from cart.models import Cart,CartItem

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleServiceSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','price','total_price']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk = cart_id).exists():
            raise serializers.ValidationError('No Cart found with this ID')
        if not CartItem.objects.filter(cart_id = cart_id).exists():
            raise serializers.ValidationError("Cart is Empty")
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True)
    class Meta:
        model = Order
        fields = ['id','user','status','total_price','created_at','updated_at','items']
        read_only_fields = ['total_price','created_at','updated_at']
        