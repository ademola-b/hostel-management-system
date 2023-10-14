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
    
    
class SchoolFeePaidStudent(models.Model):
    std_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    registration_number = models.CharField(max_length=30)
    payment_date = models.DateTimeField(auto_now_add=True)
    receipt_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.registration_number}'

class School(models.Model):
    school_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.abbr} - {self.name}"
    
class Student(models.Model):
    student_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.CharField(max_length=7, choices=level_choice)
    payment_made = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user.username} - {self.payment_made}"
    

class StudentContact(models.Model):
    contact_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    address = models.CharField(max_length=250, null=True, blank=True)
    next_of_kin_name = models.CharField(max_length=100, null=True, blank=True)
    next_of_kin_phone = models.CharField(max_length=15, null=True, blank=True)
    next_of_kin_address = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username}"

    


    

