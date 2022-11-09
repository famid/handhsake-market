from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    balance = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)


