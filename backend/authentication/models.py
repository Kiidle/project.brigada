from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    first_name = models.CharField(max_length=100, verbose_name="Vorname")