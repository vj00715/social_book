from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.

class CustomUser(AbstractUser):
    public_visibility = models.BooleanField(default=False)
    age = models.DateField(null=True)

User = get_user_model()
class Book(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    coverimg = models.ImageField(upload_to='cover/')
    bookfile = models.FileField(upload_to='book/')
    price = models.FloatField(default=0)
