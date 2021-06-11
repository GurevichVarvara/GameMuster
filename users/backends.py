"""User Backend"""
from django.contrib.auth.backends import ModelBackend


class UserBackend(ModelBackend):
    """User Backend"""

    def user_can_authenticate(self, user):
        """Reject users with active_time=None"""
        return user.active_time is not None or user.is_staff
