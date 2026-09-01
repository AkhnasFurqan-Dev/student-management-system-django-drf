"""
Enrollment model linking student to courses.
"""

from django.db import models
from django.conf import settings

from courses.models import Course


class Enrollment(models.Model):
    """Enrollment model representing a student's enrollment."""

    class Status(models.TextChoices):
        """Tracks status of the enrollment"""

        ACTIVE = "active", "Active"
        DROPPED = "dropped", "Dropped"


    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
        limit_choices_to={"role": "student"},
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")
        ordering = ["-enrolled_at"]


    def __str__(self):
        return f"{self.student.username} -> {self.course.title} ({self.status})"
