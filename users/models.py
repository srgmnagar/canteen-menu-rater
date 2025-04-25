from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=True)
    is_staff_member = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
