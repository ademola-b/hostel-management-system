from django.contrib import messages
from django.shortcuts import redirect


def redirect_anonymous_user(func):
    def wrapper_func(request, *args, **kwargs):
        
        user = request.user
        print(user)
        if user.is_anonymous:
            messages.warning(request, 'You are not authenticated, kindly login')
            return redirect('accounts:login')
        return func(request, *args, **kwargs)
    return wrapper_func
