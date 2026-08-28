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

    objects = UserManager()

    def __str__(self):
        """String representation of a user."""

        return f"{self.id}: {self.username}: is ({self.role})"