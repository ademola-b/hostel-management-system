import uuid
from django.db import models

from accounts.models import Student

# Create your models here.
class Hall(models.Model):
    hall_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=30)
    picture = models.ImageField(default='img/bld.jpeg', upload_to='img/')
    room_number = models.IntegerField()
    price = models.IntegerField(default=0)
    gender = models.CharField(max_length=8, choices=[('male', 'male'), ('female', 'female')], default='boys')
    status = models.CharField(max_length=12, choices=[('available', 'available'),('unavailable', 'unavailable')], default='available')

    def __str__(self):
        return self.name
    
class Room(models.Model):
    room_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    room_num = models.IntegerField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    max_capacity = models.IntegerField(default=4)
    current_occupancy = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.hall.name}-{self.room_num}"
    
    class Meta:
        ordering = ['room_num']


class AllocatedRooms(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.user.username} - {self.room.hall.name}"

    

