"""
Serializers for authentication, profile updates, and admin user management.
"""

from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for public self-registration.

    Accepts username, email, and password. Role defaults to STUDENT.
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create and return a new student user."""
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for profile retrieval and scoped updates via /me/ endpoint."""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "enrollment_year",
            "batch",
            "roll_number",
        ]
        read_only_fields = ["id", "role"]

    def validate(self, attrs):
        """Validate field-level edit permissions based on user role."""
        user = self.instance
        if user:
            if user.role == User.Role.TEACHER and "email" in attrs:
                if attrs["email"] != user.email:
                    raise serializers.ValidationError(
                        {"email": "Teachers cannot change their email address."}
                    )

            if user.role == User.Role.STUDENT:
                restricted_fields = {
                    "email",
                    "enrollment_year",
                    "batch",
                    "roll_number",
                    "username",
                }
                for field in restricted_fields:
                    if field in attrs and getattr(user, field) != attrs[field]:
                        raise serializers.ValidationError(
                            {field: f"Students cannot edit {field}."}
                        )

        return attrs


class AdminUserCreateSerializer(serializers.ModelSerializer):
    """Serializer used exclusively by Admins to provision Teacher and Student accounts."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "enrollment_year",
            "batch",
            "roll_number",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create user account and attach raw password temporarily for email dispatch."""
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        user._raw_password = password
        return user
