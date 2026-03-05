from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from reviews.serializers import ReviewSerializer,AllReviewSerializer
from rest_framework.decorators import action
from reviews.models import Review
from reviews.permissions import IsReviewAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from reviews.filters import ReviewFilter

# Create your views here.
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsReviewAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        try:
            serializer.save(user = self.request.user,service_id = self.kwargs.get('service_pk'))
        except IntegrityError:
            raise ValidationError({'details':'You already reviewed this service! Try editing your old one.'})
        
    
    def get_queryset(self):
        if getattr(self,'swagger_fake_view',False):
            return super().get_queryset()
        return Review.objects.filter(service_id = self.kwargs.get('service_pk'))
    
    @swagger_auto_schema(
        operation_summary='Show all Review of the service'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Create review by the users'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Update review by the reviewer'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete review by the reviewer'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Edit review by the reviewer'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Show specific review details'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
      
class AllReview(ModelViewSet):
    serializer_class = AllReviewSerializer
    # This ensures only the author can EDIT/DELETE, but anyone can VIEW
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsReviewAuthorOrReadOnly] 
    filterset_class = ReviewFilter   
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        return Review.objects.select_related('user','service').prefetch_related('service__category').all().order_by('-created_at')
      
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mine(self, request):
        # This uses the user identified by the JWT token in the header
        queryset = Review.objects.filter(user=request.user).select_related('service').order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)