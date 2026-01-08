from django.shortcuts import render
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from services.serializers import ServiceSerializer,CategorySerializer,AddServiceSerializer
from services.models import Service,Category
from django.db.models import Avg
from django.db.models.functions import Round
from django_filters.rest_framework import DjangoFilterBackend
from services.filters import ServiceFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from services.paginations import DefaultPagination
from rest_framework.permissions import SAFE_METHODS
from api.permissions import IsAdminOrReadOnly
# Create your views here.

class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.select_related('category').annotate(avg_rating=Round(Avg('review__rating'), 1)).all()
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    pagination_class = DefaultPagination
    filterset_class = ServiceFilter   
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name','description','category__name']
    ordering_fields = ['avg_rating','price']
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ServiceSerializer
        return AddServiceSerializer
    
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.annotate(service_count = Count('services')).all()
    permission_classes = [IsAdminOrReadOnly]