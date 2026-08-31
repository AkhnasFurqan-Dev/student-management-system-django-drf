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
            role=User.Role.TEACHER,
        )

        self.other_teacher = User.objects.create_user(
            username="teacher2",
            email="teacher2@example.com",
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


    #--- List Enrollment Scope Tests ---
    def test_admin_sees_all_enrollments(self):
        """Test all enrollments are shown to admin."""

        self.client.force_authenticate(self.admin)
        res = self.client.get(ENROLLMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_teacher_sees_enrollments_only_in_own_course(self):
        """Test teacher only sees all enrollments in own course."""

        self.client.force_authenticate(self.teacher)
        res = self.client.get(ENROLLMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["course"], self.own_course.id)

    def test_student_sees_own_enrollments_only(self):
        """Test a student can see only own enrollments."""

        self.client.force_authenticate(self.student)
        res = self.client.get(ENROLLMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["student"], self.student.id)


    #--- Create Enrollment Tests ---

    def test_admin_can_enroll_any_student_in_any_course(self):
        """Test admin can create an enrollment for any student in any course."""

        self.client.force_authenticate(self.admin)
        payload = {
            "student": self.other_student.id,
            "course": self.own_course.id,
        }
        res = self.client.post(ENROLLMENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_teacher_can_enroll_student_in_own_course(self):
        """Test teacher can create an enrollment for a student in own course."""

        self.client.force_authenticate(self.teacher)
        payload = {
            "student": self.other_student.id,
            "course": self.own_course.id,
        }
        res = self.client.post(ENROLLMENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_teacher_cannot_enroll_a_student_in_other_teachers_course(self):
        """Test teacher cannot create an enrollment for a student in other teacher's course."""

        self.client.force_authenticate(self.student)
        payload = {
            "student": self.other_student.id,
            "course": self.other_course.id,
        }
        res = self.client.post(ENROLLMENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_create_enrollment(self):
        """Test a student cannot create an enrollment."""

        self.client.force_authenticate(self.student)
        payload = {
            "student": self.student.id,
            "course": self.other_course.id,
        }
        res = self.client.post(ENROLLMENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_duplicate_enrollment_cannot_be_created(self):
        """Test duplicate enrollment cannot be created."""

        self.client.force_authenticate(self.admin)
        payload = {
            "student": self.student.id,
            "course": self.own_course.id,
        }
        res = self.client.post(ENROLLMENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    #--- Update Enrollment Tests ---

    def test_teacher_can_mark_enrollment_as_dropped_in_own_course(self):
        """Test a teacher can change the status of enrollment in own course."""

        self.client.force_authenticate(self.teacher)
        res = self.client.patch(
            enrollment_detail_url(self.own_enrollment.id), {"status": "dropped"}
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.own_enrollment.refresh_from_db()
        self.assertEqual(self.own_enrollment.status, Enrollment.Status.DROPPED)

    def test_teacher_cannot_modify_an_enrollment_in_other_teachers_course(self):
        """Test a teacher cannot change the status of enrollment in other teacher's course."""

        self.client.force_authenticate(self.teacher)
        res = self.client.patch(
            enrollment_detail_url(self.other_enrollment.id), {"status": "dropped"}
        )

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_student_cannot_modify_enrollment(self):
        """Test a student cannot change the status of enrollment."""

        self.client.force_authenticate(self.student)
        res = self.client.patch(
            enrollment_detail_url(self.own_enrollment.id), {"status": "dropped"}
        )

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    #--- Delete Enrollment Tests
    def test_admin_can_delete_any_enrollment(self):
        """Test an admin can delete an enrollment."""

        self.client.force_authenticate(self.admin)
        res = self.client.delete(enrollment_detail_url(self.other_enrollment.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_teacher_can_delete_an_enrollment_in_own_course(self):
        """Test a teacher can delete an enrollment in own course."""

        self.client.force_authenticate(self.teacher)
        res = self.client.delete(enrollment_detail_url(self.own_enrollment.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_teacher_cannot_delete_an_enrollment_in_other_course(self):
        """Test a teacher cannot delete an enrollment in other teacher's course."""

        self.client.force_authenticate(self.teacher)
        res = self.client.delete(enrollment_detail_url(self.other_enrollment.id))

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_cannot_access_an_enrollment(self):
        """Test an unauthorized user cannot access an enrollment."""

        res = self.client.get(ENROLLMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
