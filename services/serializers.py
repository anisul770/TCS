from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework import serializers
from services.models import Service,Category

class ServiceSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField(
        method_name= "get_avg_rating"
    )
    class Meta:
        model = Service
        fields = ['id','name','description','price','category','avg_rating','is_active']
    
    def get_avg_rating(self,service:Service):
        result = service.review_set.aggregate(avg = Round(Avg('rating'),1))['avg']
        return result or 0
    
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','description','service_count']
        
    service_count = serializers.IntegerField(read_only = True)