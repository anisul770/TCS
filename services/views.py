from django.shortcuts import render
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from services.serializers import ServiceSerializer,CategorySerializer
from services.models import Service,Category
from django.db.models import Avg
from django.db.models.functions import Round
from django_filters.rest_framework import DjangoFilterBackend
from services.filters import ServiceFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from services.paginations import DefaultPagination
from rest_framework.permissions import IsAdminUser
# Create your views here.

class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.select_related('category').annotate(avg_rating=Round(Avg('review__rating'), 1)).all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    pagination_class = DefaultPagination
    filterset_class = ServiceFilter   
    permission_classes = [IsAdminUser]
    search_fields = ['name','description','category__name']
    ordering_fields = ['avg_rating','price']
    
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.annotate(service_count = Count('services')).all()