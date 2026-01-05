from rest_framework import serializers
from services.models import Service,Category

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id','name','description','price','category','avg_rating','is_active']
        read_only_fields= ['avg_rating']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','description','service_count']
        
    service_count = serializers.IntegerField(read_only = True)