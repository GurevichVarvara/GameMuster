from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def is_email_unique(new_email):
    if User.objects.filter(email=new_email).first() or \
                User.objects.filter(unconfirmed_email=new_email).first():
        raise ValidationError(
            _('Email is not unique'),
        )


class User(AbstractUser):
    email = models.EmailField()
    birthday = models.DateField('Birthday',
                                null=True,
                                blank=True,
                                default=None)
    active_time = models.DateTimeField(null=True,
                                       default=None)
    unconfirmed_email = models.EmailField(null=True,
                                          default=None,
                                          validators=[is_email_unique])

    def user_can_authenticate(self, user):
        """
        Reject users with active_time=None.
        """

        return user.active_time is not None
