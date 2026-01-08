from reviews.models import Review
from rest_framework import serializers
from users.models import User

class SimplerUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(
        method_name="get_current_user_name"
    )
    class Meta:
        model = User
        fields = ['id','name']
    
    def get_current_user_name(self,obj):
        return obj.get_full_name()

class ReviewSerializer(serializers.ModelSerializer):
    user = SimplerUserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id','service','user','rating','comment','created_at','updated_at']
        read_only_fields = ['created_at','updated_at','service','user']