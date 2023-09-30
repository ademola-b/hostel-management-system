from django.contrib import messages
from django.shortcuts import redirect

from accounts.models import Student


def redirect_anonymous_user(func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            messages.warning(request, 'You are not authenticated, kindly login')
            return redirect('accounts:login')
        return func(request, *args, **kwargs)
    return wrapper_func

def user_profile_checker(func):
    def wrapper_func(request, *args, **kwargs):
        try:
            user = request.user
            if not user.is_warden:
                Student.objects.get(user=user)
            return func(request, *args, **kwargs)
        except Student.DoesNotExist:
            messages.warning(request, "Kindly update your profile")
            return redirect('accounts:update_profile')
    return wrapper_func

