from django.db import models
from django.contrib.auth.models import AbstractUser, User


class User(AbstractUser):
    birthday = models.DateField('Birthday',
                                null=True,
                                blank=True,
                                default=None)
    active_time = models.DateTimeField(null=True,
                                       default=None)

    def user_can_authenticate(self, user):
        """
        Reject users with active_time=None.
        """

        return user.active_time is not None
