from typing import Any
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView


from . forms import LoginForm, SignUpForm
# Create your views here.
class LoginView(View):
    template_name = "auth/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('allocation:dashboard')
                else:
                    messages.error(request, "Your account is not active, kindly contact the admin")
            else:
                messages.error(request, "Account not found")
        else:
            messages.error(request, f"An error occurred: {form.errors.as_text()}")
        
        return render(request, self.template_name, {'form':form})


def logout_request(request):
    logout(request)
    return redirect('accounts:login')

class RegisterView(CreateView):
    form_class = SignUpForm
    template_name = 'auth/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form":form})
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any):
        form = self.form_class(request.POST)
        if form.is_valid():
            print("valid")
            form.save()
            messages.success(request, "Account succesfully created")
            return redirect('accounts:login')
        else:
            messages.error(request, f"An error occured: {form.errors.as_text()}")
            return render(request, self.template_name, {'form':form})
