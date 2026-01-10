from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from djoser.views import UserViewSet as uv
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from users.serializers import AdminSetSerializer
from rest_framework.response import Response
# Create your views here.

class UserViewSet(uv):
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