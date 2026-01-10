from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from order.serializers import OrderSerializer
from django.contrib.auth import get_user_model

class UserCreateSerializer(BaseUserCreateSerializer):
    profile_pic = serializers.ImageField()
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','email','password','first_name','last_name','phone_number','bio','profile_pic','facebook_link']
        

class UserSerializer(BaseUserSerializer):
    order = OrderSerializer(many=True,read_only=True)
    profile_pic = serializers.ImageField()
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = ['id','email','first_name','last_name','phone_number','bio','profile_pic','facebook_link','order']
class AdminSetSerializer(BaseUserSerializer):
    pass