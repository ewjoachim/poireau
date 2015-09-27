from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    dropbox_token = models.CharField(max_length=127, blank=True, null=True)
