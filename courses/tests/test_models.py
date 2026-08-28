"""
Tests for the Course model.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()


class CourseModelTests(TestCase):
    """tests covering Course model."""

    def test_create_course_without_teacher(self):
        """Test course can exist without a teacher."""

        course = Course.objects.create(
            title="Computer Networks",
            description="Application of Networking",
            duration="16 weeks",
            schedule="Mon/Thu 9-11am",
        )

        self.assertIsNone(course.teacher)
        self.assertEqual(course.title, "Computer Networks")

    def test_create_course_with_teacher(self):
        """Test course can be created and linked to a teacher."""

        teacher = User.objects.create_user(
            username="teacher1",
            email="teacher1@email.com",
            password="testpass123",
            role=User.Role.TEACHER,
        )

        course = Course.objects.create(
            title="Computer Networks",
            description="Application of Networking",
            duration="16 weeks",
            schedule="Mon/Thu 9-11am",
            teacher=teacher,
        )

        self.assertEqual(course.teacher, teacher)

    def test_string_representation_returns_title(self):
        """Test string rep. of course returns its title."""

        course = Course.objects.create(
            title="Computer Networks",
            description="Application of Networking",
            duration="16 weeks",
            schedule="Mon/Thu 9-11am",
        )

        self.assertEqual(str(course), "Computer Networks")

    def test_deleting_teacher_sets_course_teacher_to_null(self):
        """If a teacher is deleted, the course must persist and course.teacher must be updated to NULL."""

        teacher = User.objects.create_user(
            username="teacher1",
            email="teacher1@email.com",
            password="testpass123",
            role=User.Role.TEACHER,
        )

        course = Course.objects.create(
            title="Computer Networks",
            description="Application of Networking",
            duration="16 weeks",
            schedule="Mon/Thu 9-11am",
            teacher=teacher,
        )

        teacher.delete()
        course.refresh_from_db()
        self.assertEqual(course.title, "Computer Networks")
        self.assertIsNone(course.teacher)