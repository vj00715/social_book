from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    custom_field = models.CharField(max_length=100, default='none')
