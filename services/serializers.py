from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework import serializers
from services.models import Service,Category

class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name','description']

class ServiceSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only = True)
    category = SimpleCategorySerializer()
    class Meta:
        model = Service
        fields = ['id','name','description','price','category','avg_rating','is_active']
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','description','service_count']
        
    service_count = serializers.IntegerField(read_only = True)