from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """User class"""

    class Role(models.TextChoices):
        """Handles assigning roles to users."""

        ADMIN = "admin", "Admin"
        TEACHER = "teacher", "Teacher"
        STUDENT = "student", "Student"

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )

    enrollment_year = models.PositiveIntegerField(null=True, blank=True)
    batch = models.CharField(max_length=50, blank=True)
    roll_number = models.CharField(max_length=20, blank=True)

    objects = UserManager()

    def __str__(self):
        """String representation of a user."""

        return f"{self.username} ({self.role})"