from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer

User = get_user_model()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get current user profile"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def oauth_callback(request):
    """
    Handle OAuth callback from frontend
    This endpoint receives the auth token and returns user data
    """
    token = request.data.get("token")

    if not token:
        return Response(
            {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Validate token and get user
        from rest_framework.authtoken.models import Token

        token_obj = Token.objects.get(key=token)
        user = token_obj.user

        serializer = UserSerializer(user)
        return Response(
            {
                "user": serializer.data,
                "token": token,
                "redirect_url": f"/{user.role}/dashboard",
            }
        )
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_user_role(request):
    """Update user role (for testing/admin purposes)"""
    role = request.data.get("role")

    if role not in ["student", "teacher", "admin"]:
        return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

    request.user.role = role
    request.user.save()

    serializer = UserSerializer(request.user)
    return Response(serializer.data)
