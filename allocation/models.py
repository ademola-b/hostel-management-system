import uuid
from django.db import models

# Create your models here.
class Hall(models.Model):
    hall_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=30)
    picture = models.ImageField(default='img/bld.jpeg', upload_to='img/')
    room_number = models.IntegerField()
    price = models.IntegerField(default=0)
    gender = models.CharField(max_length=8, choices=[('boys', 'boys'), ('girls', 'girls')], default='boys')
    status = models.CharField(max_length=12, choices=[('available', 'available'),('unavailable', 'unavailable')], default='available')

    def __str__(self):
        return self.name
    

# class Room(models.Model):
#     room_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
#     hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
#     max_capacity = models.IntegerField(default=4)
#     present_occupancy = models.IntegerField(default=0)
