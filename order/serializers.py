from rest_framework import serializers
from order.models import Order,OrderItem
from cart.serializers import SimpleServiceSerializer
from cart.models import Cart,CartItem
from order.services import OrderService

class EmptySerializer(serializers.Serializer):
    pass

class OrderItemSerializer(serializers.ModelSerializer):
    service = SimpleServiceSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','service','quantity','price','total_price']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk = cart_id).exists():
            raise serializers.ValidationError('No Cart found with this ID')
        if not CartItem.objects.filter(cart_id = cart_id).exists():
            raise serializers.ValidationError("Cart is Empty")
        return cart_id
    
    def create(self,validated_data):
        user_id = self.context.get('user_id')
        cart_id = validated_data.get('cart_id')
        try:
            order = OrderService.create_order(user_id=user_id, cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        
    def to_representation(self, instance):
        return OrderSerializer(instance).data

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True)
    class Meta:
        model = Order
        fields = ['id','user','status','items','total_price','created_at','updated_at']
        