from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import *
# Register your models here.
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_warden', 'is_active')
    search_fields = ('username',)
    ordering = ('username',)
    readonly_fields = ('date_joined', 'last_login',)

    # filter_horizontal = ()
    # list_filter = ()
    # fieldsets = ()

    fieldsets = (
        ('User Information', {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'gender', 'profile_pic')}),
        ('Permissions', {'fields': (
            'is_warden', 'is_staff', 'is_superuser', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        
    )

    add_fieldsets = (
        ('Login Details', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

admin.site.register(User,UserAdmin)
models = [Department, Student, SchoolFeePaidStudent, School, StudentContact]
for model in models:
    admin.site.register(model)
