from django.shortcuts import render
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from services.serializers import ServiceSerializer,CategorySerializer
from services.models import Service,Category
# Create your views here.

class ServiceViewSet(ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()    
    
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.annotate(service_count = Count('services')).all()