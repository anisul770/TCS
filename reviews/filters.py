from django_filters.rest_framework import FilterSet
from reviews.models import Review

class ReviewFilter(FilterSet):
    class Meta:
        model = Review
        fields = {
            'user_id' : ['exact'],
            'service_id' : ['exact'],
        }