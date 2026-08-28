"""
Views for authentication endpoints register and current user (me) profile.
"""

from rest_framework import generics, permissions
from rest_framework.response import Response

from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """handles POST /api/auth/register/ for creation of student profiles"""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    """handles GET /api/auth/me/ for view and update of current profile."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        "returns current user's records"

        return self.request.user
