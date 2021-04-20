from django.contrib.auth.backends import ModelBackend


class UserBackend(ModelBackend):

    def user_can_authenticate(self, user):
        """
        Reject users with active_time=None
        """
        return user.active_time is not None
