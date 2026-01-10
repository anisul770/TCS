from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from djoser.views import UserViewSet as uv
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from users.serializers import AdminSetSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class UserViewSet(uv):
    @swagger_auto_schema(
        operation_summary='Promote a user to Admin by other Admin'
    )
    @action(detail=True,methods=['post'],permission_classes=[IsAdminUser])
    def promote_admin(self,request,id=None):
        if request.user.is_staff:
            user = self.get_object()
            user.is_staff = True
            user.save()
            return Response({
                'details': "User promoted to admin successfully",
            })
        return Response({
                'details': "You are not allowed to promote",
            })
        
    @swagger_auto_schema(
        operation_summary='Show all the users to Admin only otherwise only the user'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Register new user'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete the account only by the owner'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='update profile'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='For partial update'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='User profile'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('order__items__service')
        if self.action == "list" and not user.is_staff:
            queryset = queryset.filter(pk=user.pk)
        return queryset

    def get_serializer_class(self):
        if self.action == 'promote_admin':
            return AdminSetSerializer
        return super().get_serializer_class()