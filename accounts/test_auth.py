"""
Tests for registration and JET authentication endpoints.
"""

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

REGISTER_URL = reverse("accounts:register")
LOGIN_URL = reverse("accounts:token_obtain_pair")
REFRESH_URL = reverse("accounts:token_refresh")
ME_URL = reverse("accounts:me")


class RegistrationTests(APITestCase):
    """Tests for registration API"""

    def test_register_creates_student_user(self):
        """Test registration creates a student user by default."""

        payload = {
            "username": "newstudent1",
            "email": "newstudent1@example.com",
            "password": "testpass123",
        }
        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username = "newstudent1")
        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertTrue(user.check_password("testpass123"))
        self.assertNotIn("password", res.data)

    def test_register_fails_with_duplicate_email(self):
        """Test registration with an email already used fails."""

        User.objects.create_user(
            username = "existinguser",
            email = "duplicate@example.com",
            password = "testpass123",
        )

        payload = {
            "username": "existinguser",
            "email": "duplicate@example.com",
            "password": "testpass123",
        }
        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_ignores_client_provided_role(self):
        """Test client attempt to set role on registration is ignored."""

        payload = {
            "username": "sneaky",
            "email": "sneaky@example.com",
            "password": "testpass123",
            "role": "admin",
        }
        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username = "sneaky")
        self.assertEqual(user.role, User.Role.STUDENT)


class LoginTests(APITestCase):
    """Tests for login API"""

    def setUp(self):
        self.user = User.objects.create_user(
            username = "loginuser",
            email = "loginuser@example.com",
            password = "testpass123",
        )

    def test_login_returns_access_and_refresh_tokens(self):
        """Test if login is successful, access is granted and tokens are returned."""

        res = self.client.post(
            LOGIN_URL, {
                "username": "loginuser",
                "email": "loginuser@example.com",
                "password": "testpass123"
            }
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_login_fails_with_wrong_pass(self):
        """Tests if login fails with wrong credentials."""

        res = self.client.post(
            LOGIN_URL, {
                "username": "loginuser",
                "email": "loginuser@example.com",
                "password": "wrongpass"
            }
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_returns_new_access_token(self):
        """Test new token is returned upon refresh."""

        login_res = self.client.post(
            LOGIN_URL, {
                "username": "loginuser",
                "email": "loginuser@example.com",
                "password": "testpass123"
            }
        )

        refresh_token = login_res.data["refresh"]
        res = self.client.post(REFRESH_URL, {"refresh": refresh_token})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)


class MeEndpointTests(APITestCase):
    """Tests for Me URL requests."""

    def setUp(self):
        self.user = User.objects.create_user(
            username = "meuser",
            email = "meuser@example.com",
            password = "testpass123",
            role = User.Role.TEACHER,
        )

    def test_me_requires_authentication(self):
        """Test login and authentication is required for requests."""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_authenticated_user_profile(self):
        """Test Me returns only profile of currently logged-in user."""

        login_res = self.client.post(
            LOGIN_URL, {
                "username": "meuser",
                "password": "testpass123",
            }
        )

        access = login_res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {access}")
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["username"], "meuser")
        self.assertEqual(res.data["role"], "teacher")