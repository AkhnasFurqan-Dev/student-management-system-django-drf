"""
Tests for course APIs
list, create, retrieve, update, delete
"""

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from courses.models import Course

User = get_user_model()

COURSES_URL = reverse("courses:course-list")

def course_detail_url(course_id):
    """helper to build detail url for a given course id"""

    return reverse("courses:course-detail", args=[course_id])


class CourseAccessTests(APITestCase):
    """Tests for Course list and create endpoints"""

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
            username="student",
            email="student@example.com",
            password="testpass123",
            role=User.Role.STUDENT,
        )

        self.own_course = Course.objects.create(
            title="Own Course",
            description="Own course description.",
            duration_value=4,
            duration_unit="week",
            schedule="Tue 8-10am",
            teacher=self.teacher,
        )

        self.other_course = Course.objects.create(
            title="Other Course",
            description="Other course description.",
            duration_value=2,
            duration_unit="week",
            schedule="Fri 3-4pm",
            teacher=self.other_teacher,
        )

    def test_student_cannot_access_course_list(self):
        """test students aren't allowed to see course list"""

        self.client.force_authenticate(self.student)
        res = self.client.get(COURSES_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_access_course_list(self):
        """test unauthenticated users aren't allowed to see course list"""

        res = self.client.get(COURSES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_sees_all_course_list(self):
        """test admin is allowed to see course list"""

        self.client.force_authenticate(self.admin)
        res = self.client.get(COURSES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_teacher_sees_own_course_list(self):
        """test teacher is allowed to see own course list"""

        self.client.force_authenticate(self.teacher)
        res = self.client.get(COURSES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Own Course")

    def test_admin_can_create_course(self):
        """test admins are allowed to create a course"""

        self.client.force_authenticate(self.admin)
        payload = {
            'title':'New Course',
            'description': 'New Course Description',
            'duration_value': 3,
            'duration_unit': 'WEEK',
            'schedule': 'Fri 8am',
        }
        res = self.client.post(COURSES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Course.objects.filter(title="New Course").exists())

    def test_teacher_cannot_create_course(self):
        """test teachers aren't allowed to create a course"""

        self.client.force_authenticate(self.teacher)
        payload = {
            'title':'Illegal Course',
            'description': 'Illegal Course Description',
            'duration_value': 3,
            'duration_unit': 'WEEK',
            'schedule': 'Fri 8am',
        }
        res = self.client.post(COURSES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_assign_teacher_via_update(self):
        """test admin can assign teacher to a course"""

        self.client.force_authenticate(self.admin)
        unassigned_course = Course.objects.create(
            title = 'Illegal Course',
            description = 'Illegal Course Description',
            duration_value = 3,
            duration_unit = "week",
            schedule = 'Fri 8am',
        )
        res = self.client.patch(
            course_detail_url(unassigned_course.id), {"teacher": self.teacher.id}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        unassigned_course.refresh_from_db()
        self.assertEqual(unassigned_course.teacher, self.teacher)

    def test_teacher_cannot_update_course(self):
        """test teacher isn't allowed to update a course"""

        self.client.force_authenticate(self.teacher)
        res = self.client.patch(
            course_detail_url(self.own_course.id), {"title": "Changed Title"}
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_course(self):
        """test admin can delete a course"""

        self.client.force_authenticate(self.admin)
        res = self.client.delete(course_detail_url(self.own_course.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=self.own_course.id).exists())

    def test_teacher_cannot_delete_course(self):
        """test students aren't allowed to see course list"""

        self.client.force_authenticate(self.teacher)
        res = self.client.delete(course_detail_url(self.own_course.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_cannot_view_other_teachers_course_details(self):
        """test students aren't allowed to see course list"""

        self.client.force_authenticate(self.teacher)
        res = self.client.get(course_detail_url(self.other_course.id))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
