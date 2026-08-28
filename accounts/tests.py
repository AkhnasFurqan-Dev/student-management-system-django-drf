"""
Tests for User Model
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):
    """User Model Test Class"""

    def test_create_user_with_default_role_student(self):
        """Test creating a default user with default role student."""

        user = User.objects.create_user(
            username = 'student1',
            email = 'student1@example.com',
            password = 'testpass123',
        )

        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertTrue(user.check_password("testpass123"))

    def test_create_user_with_teacher_role(self):
        """Test creating a user with role teacher."""

        user = User.objects.create_user(
            username = 'teacher1',
            email = 'teacher1@example.com',
            password = 'testpass123',
        )

        self.assertEqual(user.role, User.Role.TEACHER)

    def test_create_superuser_has_admin_role(self):
        """Test creating a superuser with admin role."""

        admin = User.objects.create_user(
            username = 'admin1',
            email = 'admin1@example.com',
            password = 'testpass123',
        )

        self.assertEqual(admin.role, User.Role.ADMIN)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_role_choices_are_exactly_three(self):
        """Test that available roles are only three (student, teacher, admin)"""

        roles = [choice[0] for choice in User.Role.choices]

        self.assertEqual(set(roles), {"admin", "teacher", "student"})

    def test_string_representation_includes_username_and_role(self):
        """Test that string representation returns username and role."""

        user = User.objects.create_user(
            username = 'student1',
            email = 'student1@example.com',
            password = 'testpass123',
        )

        self.assertIn("student1", str(user))
        self.assertIn("student", str(user))
