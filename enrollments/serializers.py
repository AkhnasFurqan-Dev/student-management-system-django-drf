"""
Serializers for the enrollment model
"""

from rest_framework import serializers

from django.contrib.auth import get_user_model

from courses.models import Course

from .models import Enrollment

User = get_user_model()


class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Handles create, update and list Enrollments.
    Ensures student field accepts only users with STUDENT role.
    Ensures teachers can only create enrollments for their own courses.
    """

    student = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.Role.STUDENT)
    )

    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all()
    )


    class Meta:
        model = Enrollment
        fields = ["id", "student", "course", "status", "enrolled_at"]
        read_only_fields = ["id", "enrolled_at"]


    def validate(self, attrs):
        request = self.context.get("request")
        course = attrs.get("course")

        if request and request.user.role == User.Role.TEACHER and course:
            if course.teacher != request.user:
                raise serializers.ValidationError(
                    {"course": "Teachers can only enroll students in their own course(s)."}
                )

        return attrs
