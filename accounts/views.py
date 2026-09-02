from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response

from django.core.mail import send_mail
from django.conf import settings

from accounts.permissions import IsAdmin, IsAdminOrTeacher

from .models import User

from .serializers import RegisterSerializer, UserProfileSerializer, AdminUserCreateSerializer

from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema(
    summary="Register a new user",
    description=(
        "Creates a new student account. Registration is publicly accessible and does not require authentication. The password must be at least 8 characters long."
    ),
)
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema_view(
    get=extend_schema(
        summary="Get current user profile",
        description=(
            "Returns the profile of the currently authenticated user. Authentication using a valid JWT access token is required."
        ),
    ),
    patch=extend_schema(
        summary="Partially update current user profile",
        description=(
            "Partially updates the profile of the currently authenticated user. Only permitted profile fields can be modified."
        ),
    ),
    put=extend_schema(
        summary="Update current user profile",
        description=(
            "Updates the profile of the currently authenticated user. The fields that can be modified depend on the user's role."
        ),
    ),
)
class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema_view(
    list=extend_schema(
        summary="List users",
        description=(
            "Returns a list of users. Administrators can view all users, while teachers can view students enrolled in their courses."
        ),
    ),
    retrieve=extend_schema(
        summary="Retrieve a user",
        description=(
            "Returns the details of a specific user. Administrators can retrieve any user, while teachers can retrieve students enrolled in their courses."
        ),
    ),
    create=extend_schema(
        summary="Create a user",
        description=(
            "Creates a new user. Only administrators can create users through this endpoint. The password is set during creation and the user's role can be specified."
        ),
    ),
    update=extend_schema(
        summary="Update a user",
        description=(
            "Replaces a user's information. Only administrators can update users."
        ),
    ),
    partial_update=extend_schema(
        summary="Partially update a user",
        description=(
            "Updates selected fields of a user. Only administrators can modify users through this endpoint."
        ),
    ),
    destroy=extend_schema(
        summary="Delete a user",
        description=(
            "Deletes a user from the system. Only administrators can delete users."
        ),
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    Endpoints for admins to manage users and teachers to view their students.
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
