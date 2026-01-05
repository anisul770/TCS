from django.shortcuts import render
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from services.serializers import ServiceSerializer,CategorySerializer
from services.models import Service,Category
from django.db.models import Avg
from django.db.models.functions import Round
# Create your views here.

class ServiceViewSet(ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.annotate(avg_rating=Round(Avg('review__rating'), 1)).all()
    
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.annotate(service_count = Count('services')).all()