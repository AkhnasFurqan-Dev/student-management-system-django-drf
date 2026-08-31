"""
Tests for Enrollment API CRUD endpoints.
"""

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course
from enrollments.models import Enrollment


User = get_user_model()

ENROLLMENT_URL = reverse("enrollments:enrollment-list")


def enrollment_detail_url(enrollment_id):
    """Helper func. to detail url for a given enrollment ID."""

    return reverse("enrollments:enrollment-detail", args=[enrollment_id])


class EnrollmentAccessTests(APITestCase):
    """Tests for role-scoped access to Enrollment API."""

    def setUp(self):

        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="testpass123",
        )

        self.teacher = User.objects.create_user(
            username="teacher1",
            email="teacher1@example.com",
            password="testpass123",
        )

        self.other_teacher = User.objects.create_user(
            username="teacher2",
            email="teacher2@example.com",
            password="testpass123",
            role=User.Role.TEACHER,
        )

        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="testpass123",
            role=User.Role.TEACHER,
        )

        self.student = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="testpass123",
            role=User.Role.STUDENT,
        )

        self.other_student = User.objects.create_user(
            username="student2",
            email="student2@example.com",
            password="testpass123",
            role=User.Role.STUDENT,
        )

        self.own_course = Course.objects.create(
            title="Own Course",
            description="Own course description",
            duration="4 weeks",
            schedule="Mon 10am",
            teacher=self.teacher,
        )

        self.other_course = Course.objects.create(
            title="Other Course",
            description="Other course description",
            duration="6 weeks",
            schedule="Wed 10am",
            teacher=self.other_teacher,
        )

        self.own_enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.own_course,
        )

        self.other_enrollment = Enrollment.objects.create(
            student=self.other_student,
            course=self.other_course,
        )