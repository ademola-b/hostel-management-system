from django.contrib import admin
from .models import Hall, Room, AllocatedRooms
# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display = ["hall", "room_num", "max_capacity", "current_occupancy"]


admin.site.register(Hall)
admin.site.register(Room, RoomAdmin)
admin.site.register(AllocatedRooms)