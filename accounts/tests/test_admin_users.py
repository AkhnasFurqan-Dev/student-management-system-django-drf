"""
Tests for Admin user management endpoints: creating teachers/students
with credentials emailed, and viewing user profile lists.
"""
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

USERS_URL = reverse("accounts:user-list")


class AdminUserManagementTests(APITestCase):
    """Tests admin-only user creation and user listing."""

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin_mgr", email="admin_mgr@example.com", password="pass12345"
        )
        self.teacher = User.objects.create_user(
            username="teacher_mgr", email="teacher_mgr@example.com", password="pass12345",
            role=User.Role.TEACHER
        )
        self.student = User.objects.create_user(
            username="student_mgr", email="student_mgr@example.com", password="pass12345",
            role=User.Role.STUDENT
        )
        mail.outbox = []

    def test_admin_can_create_teacher_and_sends_credentials_email(self):
        """Admin creates a teacher account; system emails login credentials."""
        self.client.force_authenticate(self.admin)
        payload = {
            "username": "new_teacher",
            "email": "new_teacher@example.com",
            "password": "securepassword123",
            "role": "teacher",
        }
        res = self.client.post(USERS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        created_user = User.objects.get(username="new_teacher")
        self.assertEqual(created_user.role, User.Role.TEACHER)

        # Check credentials email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["new_teacher@example.com"])
        self.assertIn("securepassword123", mail.outbox[0].body)

    def test_admin_can_create_student_with_profile_fields(self):
        """Admin creates a student account with enrollment year, batch, and roll number."""
        self.client.force_authenticate(self.admin)
        payload = {
            "username": "new_student",
            "email": "new_student@example.com",
            "password": "securepassword123",
            "role": "student",
            "enrollment_year": 2026,
            "batch": "CS-2026",
            "roll_number": "CS-001",
        }
        res = self.client.post(USERS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        created_user = User.objects.get(username="new_student")
        self.assertEqual(created_user.enrollment_year, 2026)
        self.assertEqual(created_user.batch, "CS-2026")
        self.assertEqual(created_user.roll_number, "CS-001")

    def test_non_admin_cannot_create_users(self):
        """Teachers and students cannot create users via this endpoint."""
        self.client.force_authenticate(self.teacher)
        payload = {
            "username": "unauthorized_user",
            "email": "unauth@example.com",
            "password": "securepassword123",
            "role": "student",
        }
        res = self.client.post(USERS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
