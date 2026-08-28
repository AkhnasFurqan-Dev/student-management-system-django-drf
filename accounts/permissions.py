"""
Role-based permission classes.

views utilizing this: accounts, courses, enrollment
"""

from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Allows access only to users with Role as ADMIN."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == request.user.Role.ADMIN
        )


class IsTeacher(BasePermission):
    """Allows access only to users with Role as TEACHER."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == request.user.Role.TEACHER
        )


class IsStudent(BasePermission):
    """Allows access only to users with Role as STUDENT."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == request.user.Role.STUDENT
        )


class IsAdminOrTeacher(BasePermission):
    """Allows access only to users with Role as ADMIN or TEACHER."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in (request.user.Role.ADMIN, request.user.Role.TEACHER)
        )