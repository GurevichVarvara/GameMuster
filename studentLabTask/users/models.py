from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birthday = models.DateField('Birthday', null=True, default=None)
    active_time = models.DateTimeField(null=True, default=None)
