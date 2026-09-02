"""
Tests for course and enrollment emails.
"""

from django.core import mail
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course
from enrollments.models import Enrollment

User = get_user_model()


class NotificationTests(APITestCase):
    """Tests email notifications triggered by course assignments and enrollments."""

    def setUp(self):

        self.admin = User.objects.create_superuser(
            username="admin_notify",
            email="admin_notify@example.com",
            password="testpass123",
        )

        self.teacher = User.objects.create_user(
            username="teacher_notify",
            email="teacher_notify@example.com",
            password="testpass123",
            role=User.Role.TEACHER,
        )

        self.student = User.objects.create_user(
            username="student_notify",
            email="student_notify@example.com",
            password="testpass123",
            role=User.Role.STUDENT,
        )

        self.course = Course.objects.create(
            title="Notify Test Course",
            description="Notify Course Description",
            duration_value=1,
            duration_unit="week",
            schedule="Fri 9am",
        )

        mail.outbox = []

    def test_email_sent_when_teacher_assigned_to_course(self):
        """Test updating a course's teacher triggers an email to assigned teacher."""

        self.client.force_authenticate(self.admin)
        url = reverse("courses:course-detail", args={self.course.id})
        res = self.client.patch(url, {"teacher": self.teacher.id})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.teacher.email])
        self.assertIn(self.course.title, mail.outbox[0].subject)

    def test_email_sent_to_student_on_enrollment(self):
        """Test enrolling a student triggers an email to enrolled student."""

        self.client.force_authenticate(self.admin)
        url = reverse("enrollments:enrollment-list")
        res = self.client.post(url, {"student": self.student.id, "course": self.course.id})

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.student.email])
        self.assertIn("Enrollment", mail.outbox[0].subject)


    def test_email_sent_to_student_on_enrollment_status_change(self):
        """Test updating enrollment status triggers an email to the student."""

        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
        )
        mail.outbox = []

        self.client.force_authenticate(self.admin)
        url = reverse("enrollments:enrollment-detail", args={enrollment.id})
        res = self.client.patch(url, {"status": "dropped"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.student.email])
        self.assertIn("Status Updated", mail.outbox[0].subject)
