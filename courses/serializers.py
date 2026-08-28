"""
Serializer for Course model.
"""

from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Course

User = get_user_model()


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course"""

    teacher = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.Role.TEACHER),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Course
        fields = [
            "id", "title", "description", "duration", "schedule", "teacher", "created_at", "updated-at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
