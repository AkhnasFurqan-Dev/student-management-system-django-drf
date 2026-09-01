from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response

from django.core.mail import send_mail
from django.conf import settings

from accounts.permissions import IsAdmin, IsAdminOrTeacher

from .models import User

from .serializers import RegisterSerializer, UserProfileSerializer, AdminUserCreateSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    """
    Endpoints for Admin to manage all users. and Teachers to view their students.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):

        if self.action in ["list", "retrieve"]:
            return [permissions.IsAuthenticated(), IsAdminOrTeacher()]

        return [permissions.IsAuthenticated(), IsAdmin()]

    def get_queryset(self):

        user = self.request.user

        if user.role == user.Role.ADMIN:
            return User.objects.all()
        elif user.role == user.Role.TEACHER:
            return User.objects.filter(
                role=user.Role.STUDENT,
                enrollments__course__teacher=user,
            ).distinct()

        return User.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return AdminUserCreateSerializer
        return UserProfileSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        raw_password = getattr(user, "_raw_password", None)

        if raw_password:
            send_mail(
                subject="Your Student Management System Account Credentials",
                message=(
                    f"Hello {user.username},\n\n"
                    f"An '{user.role}' account has been created for you.\n\n"
                    f"Username: {user.username}\n"
                    f"Password: {raw_password}\n\n"
                    f"Please log in and update your password."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
