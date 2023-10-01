import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    profile_pic = models.ImageField(upload_to='profile_pic/')
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=7, choices=[('male', 'male'),('female', 'female')], default='other')
    is_warden = models.BooleanField(default=False)


    def __str__(self):
        return self.username

level_choice = [
    ('ND I', 'ND I'),
    ('ND II', 'ND II'),
    ('HND I', 'HND I'),
    ('HND II', 'HND II')
]

class Department(models.Model):
    dept_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Student(models.Model):
    student_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.CharField(max_length=7, choices=level_choice)
    payment_made = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.payment_made}"
    

