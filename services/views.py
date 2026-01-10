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
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class ServiceViewSet(ModelViewSet):
    """
    This is The API Endpoint for managing services
    - Allow admin to manage all services
    - Allows users to browse through the available services
    """
    queryset = Service.objects.select_related('category').annotate(avg_rating=Round(Avg('review__rating'), 1)).all()
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    pagination_class = DefaultPagination
    filterset_class = ServiceFilter   
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name','description','category__name']
    ordering_fields = ['avg_rating','price']
    
    
    @swagger_auto_schema(
        operation_summary='Show all the services'
    )
    def list(self, request, *args, **kwargs):
        """Retrieve All the services"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Create new services by Admin',
        operation_description="Add new service by Admin"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ServiceSerializer
        return AddServiceSerializer
    
    @swagger_auto_schema(
        operation_summary='Show a service details'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Update service details by admin'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete a service by admin'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Partial update service info by admin'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    
class CategoryViewSet(ModelViewSet):
    """
    This is The API Endpoint for managing Category
    - Allow admin to manage all Category
    - Allows users to browse through the available Category
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.annotate(service_count = Count('services')).all()
    permission_classes = [IsAdminOrReadOnly]
    
    @swagger_auto_schema(
        operation_summary='Show all the Category'
    )
    def list(self, request, *args, **kwargs):
        """Retrieve All the Category"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Create new category by Admin'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Show the specific category details'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Update specific category details by admin'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Partial update specific category by admin'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete specific category by admin'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    