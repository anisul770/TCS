from rest_framework import serializers
from cart.models import Cart,CartItem
from services.models import Service

class SimpleServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id','name','price','category']

class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','service','quantity']
        
    def save(self,**kwargs):
        cart_id = self.context['cart_id']
        service_id = self.validated_data['service'].id
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id,service_id=service_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id,service_id=service_id,quantity=quantity)
        return self.instance

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']            
            
class CartItemSerializer(serializers.ModelSerializer):
    service = SimpleServiceSerializer()
    total_price = serializers.SerializerMethodField(
        method_name="get_total_price"
    )
    class Meta:
        model = CartItem
        fields = ['id','service','quantity','total_price']
        
    def get_total_price(self,cart_item : CartItem):
        return cart_item.quantity * cart_item.service.price

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many = True,read_only = True)
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price'
    )
    class Meta:
        model = Cart
        fields = ['id','user','items','total_price']
        read_only_fields = ['user']

    def get_total_price(self,cart:Cart):
        return sum([item.service.price * item.quantity for item in cart.items.all()])