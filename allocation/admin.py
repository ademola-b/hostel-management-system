from django.contrib import admin
from .models import Hall, Room, AllocatedRooms
# Register your models here.
admin.site.register(Hall)
admin.site.register(Room)
admin.site.register(AllocatedRooms)