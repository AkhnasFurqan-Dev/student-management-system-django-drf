"""
Views for Enrollment APIs with role-based scope.
"""

from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework import viewsets, permissions, exceptions

from accounts.permissions import IsAdminOrTeacher

from .models import Enrollment

from .serializers import EnrollmentSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List enrollments",
        description=(
            "Admins can view all enrollments. Teachers can view only enrollments assigned to them."
        ),
    ),
    retrieve=extend_schema(
        summary="Retrieve an enrollment",
        description=(
            "Returns details for an enrollment. Teachers and Students can retrieve only enrollments related to them."
        ),
    ),
    create=extend_schema(
        summary="Create an enrollment",
        description=(
            "Admins can enroll any student in any course. Only admins can create an enrollment."
        ),
    ),
    update=extend_schema(
        summary="Update an enrollment",
        description=(
            "Replaces an existing enrollment. Only admins and teachers can update an enrollment."
        ),
    ),
    partial_update=extend_schema(
        summary="Partially updates an enrollment",
        description=(
            "Updates a selected enrollment's fields. Only admins and teachers can update an enrollment."
        ),
    ),
    destroy=extend_schema(
        summary="Delete an enrollment",
        description=(
            "Deletes an enrollment. Only admins and teachers can delete an enrollment."
        ),
    ),
)
class EnrollmentViewSet(viewsets.ModelViewSet):

    serializer_class = EnrollmentSerializer

    def get_permissions(self):
        """Sets permissions for roles"""

        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsAdminOrTeacher()]

        return [permissions.IsAuthenticated()]

    def get_queryset(self):

        user = self.request.user

        if user.role == user.Role.ADMIN:
            return Enrollment.objects.all()
        elif user.role == user.Role.TEACHER:
            return Enrollment.objects.filter(course__teacher=user)
        elif user.role == user.Role.STUDENT:
            return Enrollment.objects.filter(student=user)
        return Enrollment.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        course = serializer.validated_data.get("course")

        if user.role == user.Role.TEACHER and course.teacher != user:
            raise exceptions.PermissionDenied(
                "You cannot enroll students into courses you do not teach."
            )

        serializer.save()
