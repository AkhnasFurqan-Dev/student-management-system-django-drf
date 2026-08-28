"""
Views for the Courses API
"""

from rest_framework import viewsets, permissions

from accounts.permissions import IsAdmin, IsAdminOrTeacher
from .models import Course
from .serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):

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
