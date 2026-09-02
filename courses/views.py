"""
Views for the Courses API
"""

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes

from rest_framework import viewsets, permissions

from accounts.permissions import IsAdmin, IsAdminOrTeacher
from .models import Course
from .serializers import CourseSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List courses",
        description=(
            "Admins can view all course. Teachers can view only courses assigned to them."
        ),
    ),
    retrieve=extend_schema(
        summary="Retrieve a course",
        description=(
            "Returns details for a course. Teachers can retrieve only courses assigned to them."
        ),
    ),
    create=extend_schema(
        summary="Create a course",
        description=(
            "Create a new course, Only admins can create a course."
        ),
    ),
    update=extend_schema(
        summary="Update a course",
        description=(
            "Replaces an existing course with new inputs. Only admins can update a course."
        ),
    ),
    partial_update=extend_schema(
        summary="Partially update a course",
        description=(
            "Updates a selected course's fields. Only admins can update a course."
        ),
    ),
    destroy=extend_schema(
        summary="Delete a course",
        description=(
            "Deletes a course. Only admins can delete a course."
        ),
    ),
)
class CourseViewSet(viewsets.ModelViewSet):
    """API endpoints for managing courses with role-based access."""

    serializer_class = CourseSerializer

    def get_permissions(self):

        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsAdmin()]

        return [permissions.IsAuthenticated(), IsAdminOrTeacher()]

    def get_queryset(self):
        user = self.request.user

        if user.role == user.Role.ADMIN:
            return Course.objects.all()

        return Course.objects.filter(teacher=user)
