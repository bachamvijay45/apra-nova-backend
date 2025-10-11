from rest_framework import serializers
from .models import CustomUser
from dj_rest_auth.registration.serializers import SocialLoginSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "role", "profile_image", "created_at"]
        read_only_fields = ["id", "created_at"]


class CustomSocialLoginSerializer(SocialLoginSerializer):
    """Custom serializer to include user role in social login response"""
    
    def get_response_data(self, user):
        data = super().get_response_data(user)
        data['role'] = user.role
        data['redirect_url'] = f"/{user.role}/dashboard"
        return data