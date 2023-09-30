import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    profile_pic = models.ImageField(upload_to='profile_pic/')
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_warden = models.BooleanField(default=False)

level_choice = [
    ('', ''),
    ('', ''),
    ('', ''),
    ('', '')
]

# class Student(models.Model):
#     student_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     department = models.CharField()
#     level = models.CharField(max_length=5, choices=level_choice)
#     payment_made = models.BooleanField(default=False)

