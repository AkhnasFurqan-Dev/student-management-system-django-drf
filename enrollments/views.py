"""
Views for Enrollment APIs wth role-based scope.
"""

from rest_framework import viewsets, permissions, exceptions

from accounts.permissions import IsAdmin, IsAdminOrTeacher, IsStudent, IsTeacher

from .models import Enrollment

from .serializers import EnrollmentSerializer


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

        if user.role==user.Role.TEACHER and course.teacher != user:
            raise exceptions.PermissionDenied(
                "You cannot enroll students into courses you do not teach."
            )

        serializer.save()
