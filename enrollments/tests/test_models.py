"""
Tests for Enrollment model.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from courses.models import Course
from enrollments.models import Enrollment

User = get_user_model()


class EnrollmentModelTests(TestCase):
    """Tests covering Enrollment model"""

    def setUp(self):

        self.teacher = User.objects.create_user(
            username="teacher1",
            email="teacher1@example.com",
            password="testpass123",
            role=User.Role.TEACHER,
        )

        self.student = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="testpass123",
            role=User.Role.STUDENT,
        )

        self.course = Course.objects.create(
            title="Sample Course",
            description="Sample course description.",
            duration="4 weeks",
            schedule="Tue 8-10am",
            teacher=self.teacher,
        )


    def test_create_enrollment_defaults_to_active_status(self):
        """Test new enrollment defaults to active unless specified otherwize"""

        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
        )
        self.assertEqual(enrollment.status, Enrollment.Status.ACTIVE)

    def test_cannot_enroll_same_student_in_same_course_twice(self):
        """Test unique enrollment and prevent duplicate."""

        Enrollment.objects.create(
            student=self.student,
            course=self.course,
        )
        with self.assertRaises(IntegrityError):
            Enrollment.objects.create(
                student=self.student,
                course=self.course
            )

    def test_string_representation_shows_student_and_course(self):
        """Test string rep. returns course title and student name"""

        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
        )
        self.assertIn("student1", str(enrollment))
        self.assertIn("Sample Course", str(enrollment))

    def test_can_mark_enrollment_as_dropped(self):
        """Test enrollment can be changed to dropped."""

        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
        )
        enrollment.status = Enrollment.Status.DROPPED
        enrollment.save()
        enrollment.refresh_from_db()
        self.assertEqual(enrollment.status, Enrollment.Status.DROPPED)