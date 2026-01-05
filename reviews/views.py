from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from reviews.serializers import ReviewSerializer
from reviews.models import Review

# Create your views here.
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    
    def perform_create(self, serializer):
        try:
            serializer.save(user = self.request.user,service_id = self.kwargs.get('service_pk'))
        except IntegrityError:
            raise ValidationError({'details':'You already reviewed this service! Try editing your old one.'})
        
    
    def get_queryset(self):
        return Review.objects.filter(service_id = self.kwargs.get('service_pk'))