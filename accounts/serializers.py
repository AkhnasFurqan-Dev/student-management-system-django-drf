"""
Serilaizers for user registration and profile representation.
"""

from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for public self registration.

    Write fields are "username", "email", "password".
    "role" field is ignored, default is STUDENT.
    """

    password = serializers.CharField(write_only = True, min_length = 8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create user"""

        user = User.objects.create_user(
            username = validated_data["username"],
            email = validated_data["email"],
            password = validated_data["password"],
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    """User serializer for ME_URL requests"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role"]
        read_only_fields = ["id", "role"]
