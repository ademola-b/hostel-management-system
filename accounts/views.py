from typing import Any
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, UpdateView

from allocation.models import AllocatedRooms


from . forms import LoginForm, SignUpForm, UserUpdateProfileForm, StudentProfileForm, StudentContactForm
from . models import User, Student, StudentContact, SchoolFeePaidStudent, Department
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
                if user.is_superuser:
                    return redirect('accounts:admin_page')
                if user.is_active:
                    print(f"profile - {user.profile_pic}")
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
            existing_payments = SchoolFeePaidStudent.objects.filter(registration_number = request.POST['username']).first()

            if existing_payments:
                form.save()
                messages.success(request, "Account succesfully created")
                return redirect('accounts:login')
            else:
                messages.error(request, "The provided registration number has not school fee record, contact your student affair if other wise.")
        else:
            messages.error(request, f"An error occured: {form.errors.as_text()}")
        return render(request, self.template_name, {'form':form})
        
class ProfileView(View):
    def get(self, request):
        form = UserUpdateProfileForm(request)
        user = request.user
        try:
            alloc = AllocatedRooms.objects.get(student=user.student)
            return render(request, "hostel/profile.html", {'form':form, 'user':user, 'alloc':alloc})
        except:
            return render(request, "hostel/profile.html", {'form':form, 'user':user})


def load_departments(request):
    school_id = request.GET.get('school')
    print(f"sx: {school_id}")
    departments = Department.objects.filter(school__school_id = school_id)
    print(f"dap: {departments}")
    return render(request, 'utils/depts_dropdown_list_options.html', {'depts':departments})

class UpdateProfileView(UpdateView):
    template_name = "auth/update_profile.html"

    form_class = UserUpdateProfileForm
    second_form_class = StudentProfileForm
    third_form_class = StudentContactForm

    def get(self, request):
        form1 = self.form_class(request)
        form2 = self.second_form_class()
        form3 = self.third_form_class()
        return render(request, self.template_name, {'form1':form1, 'form2':form2, 'form3':form3})
    
    def post(self, request):
        form1 = self.form_class(request, request.POST, request.FILES)
        form2 = self.second_form_class(request.POST)
        form3 = self.third_form_class(request.POST)

        if 'update_btn' in request.POST:
            if form1.is_valid() and form2.is_valid() and form3.is_valid():
                instance1 = form1.save(commit=False)
                instance2 = form2.save(commit=False)

                student = Student.objects.create(
                    user = request.user,
                    school = form2.cleaned_data['school'],
                    department = form2.cleaned_data['department'],
                    level = form2.cleaned_data['level']
                )

                StudentContact.objects.create(
                    student = student,
                    address = form3.cleaned_data['address'],
                    next_of_kin_name = form3.cleaned_data['next_of_kin_name'],
                    next_of_kin_phone = form3.cleaned_data['next_of_kin_phone'],
                    next_of_kin_address = form3.cleaned_data['next_of_kin_address']
                )

                user = User.objects.get(user_id = request.user.user_id)

                user.first_name = form1.cleaned_data['first_name']
                user.last_name = form1.cleaned_data['last_name']
                user.middle_name = form1.cleaned_data['middle_name']
                user.dob = form1.cleaned_data['dob']
                user.blood_group = form1.cleaned_data['blood_group']
                user.phone = form1.cleaned_data['phone']
                user.profile_pic = form1.cleaned_data['profile_pic']
                user.gender = form1.cleaned_data['gender']
                user.save()
                messages.success(request, "Profile Successfully Updated, You can proceed with your application")
                return redirect("allocation:hostel-list")
            else:
                messages.error(request, f"{form1.errors.as_text()} {form2.errors.as_text()}")
                return render(request, self.template_name, {'form1':form1, 'form2':form2, 'form3':form3})
        else:
            school = request.POST.get('school')
            print(f"school: {school}")
            # department_field = request.POST.get('department')
            department = Department.objects.filter(school=school)
            form2.fields['department'].queryset = department
            return render(request, self.template_name, {'form1':form1, 'form2':form2, 'form3':form3})
            
        
