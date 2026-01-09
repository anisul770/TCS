from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from djoser.views import UserViewSet as uv
from django.conf import settings
# Create your views here.

class UserViewSet(uv):
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('order__items__service')
        if self.action == "list" and not user.is_staff:
            queryset = queryset.filter(pk=user.pk)
        return queryset
