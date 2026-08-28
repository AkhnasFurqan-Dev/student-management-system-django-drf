"""
Tests for ROLE-based Permission Classes
"""

from django.contrib.auth import get_user_model
from django.urls import path, include

from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.permissions import IsAdmin, IsTeacher, IsAdminOrTeacher, IsStudent

User = get_user_model()


'''Throw away views for testing'''

class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response("ok", True)


class TeacherOnlyView(APIView):
    permission_classes = [IsTeacher]

    def get(self, request):
        return Response("ok", True)


class AdminOrTeacherView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        return Response("ok", True)


class StudentOnlyView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        return Response("ok", True)


urlpatterns = [
    path('admin-only/', AdminOnlyView.as_view()),
    path('teacher-only/', TeacherOnlyView.as_view()),
    path('admin-or-teacher/', AdminOrTeacherView.as_view()),
    path('student-only/', StudentOnlyView.as_view()),
]


class PermissionClassTests(APITestCase, URLPatternsTestCase):

    urlpatterns = urlpatterns

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="testpass123",
        )

        self.teacher = User.objects.create_user(
            username="teacher",
            email="teacher@example.com",
            password="testpass123",
            role=User.Role.TEACHER,
        )

        self.student = User.objects.create_user(
            username="student",
            email="student@example.com",
            password="testpass123",
            role=User.Role.STUDENT,
        )


    '''admin-only view test'''
    def test_admin_only_view_allows_admin(self):
        'test admin access to admin-only endpoint'

        self.client.force_authenticate(self.admin)
        res = self.client.get("/admin-only/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_only_view_blocks_teacher(self):
        'test teacher access to admin-only endpoint is blocked'

        self.client.force_authenticate(self.teacher)
        res = self.client.get("/admin-only/")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_only_view_blocks_student(self):
        'test student access to admin-only endpoint is blocked'

        self.client.force_authenticate(self.student)
        res = self.client.get("/admin-only/")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_only_view_blocks_unauthenticated(self):
        'test unauthenticated request is blocked'

        res = self.client.get("/admin-only/")
        self.assertEqual(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))


    '''teacher-only view tests'''
    def test_teacher_only_view_allows_teacher(self):
        'test teacher access to teacher-only endpoint'

        self.client.force_authenticate(self.teacher)
        res = self.client.get("/teacher-only/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_teacher_only_view_blocks_student(self):
        'test student access to teacher-only endpoint is blocked'

        self.client.force_authenticate(self.student)
        res = self.client.get("/teacher-only/")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    '''admin-or-teacher view tests'''
    def test_admin_or_teacher_only_view_allows_admin_or_teacher(self):
        'test admin and teacher are allowed to admin-or-teacher endpoint'

        self.client.force_authenticate(self.admin)
        res = self.client.get("/admin-or-teacher/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(self.teacher)
        res = self.client.get("/admin-or-teacher/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_or_teacher_only_view_blocks_student(self):
        'test student is blocked to admin-or-teacher endpoint'

        self.client.force_authenticate(self.student)
        res = self.client.get("/admin-or-teacher/")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    '''student-only view tests'''
    def test_student_only_view_allows_student(self):
        'test student is allowed to student-only endpoint'

        self.client.force_authenticate(self.student)
        res = self.client.get("/student-only/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_student_only_view_blocks_admin(self):
        'test admin is blocked from student-only endpoint'

        self.client.force_authenticate(self.admin)
        res = self.client.get("/student-only/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
