from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Student, Department

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'id': 'exampleInputEmail1','class':'form-control form-control-lg', 'placeholder':'Email', 'autofocus': 'true'}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'id':'exampleInputPassword1','class':'form-control form-control-lg', 'placeholder':'Password'}))


class SignUpForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your registration number'}))
    email = forms.EmailField(required=True, max_length=254, help_text='Enter a valid email address', widget=forms.EmailInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder':'Enter your Email Address'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder':'Enter your Email Address'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder':'Enter your Email Address'}))

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
        ]

class UserUpdateProfileForm(forms.ModelForm):

    gender_choices = [
        ('male', 'male'),
        ('female', 'female')
    ]

    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your first name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your last name'}))
    email = forms.EmailField(required=False, max_length=254, help_text='Enter a valid email address', widget=forms.EmailInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder':'Enter your Email Address', 'disabled':'disabled'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your phone number'}))
    gender = forms.ChoiceField(required=True, choices=gender_choices, widget=forms.Select(attrs={
        'class': 'form-control select form-select'
    }))

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "profile_pic",
            "phone",
            "gender"
        ]
    
    def __init__(self, request, *args, **kwargs):
        super(UserUpdateProfileForm, self).__init__(*args, **kwargs)

        self.fields['email'].initial = request.user.email

class StudentProfileForm(forms.ModelForm):

    level_choice = [
    ('ND I', 'ND I'),
    ('ND II', 'ND II'),
    ('HND I', 'HND I'),
    ('HND II', 'HND II')
    ]

    department = forms.ModelChoiceField(required=True, queryset=Department.objects.all(), empty_label="Select Department", widget=forms.Select(
        attrs={
            'class': 'form-control select form-select'
        }
    ))
    level = forms.ChoiceField(required=True, choices=level_choice, widget=forms.Select(
        attrs={
            'class': 'form-control select form-select'
        }
    ))

    class Meta:
        model = Student
        fields = [
            "department",
            "level"
        ]

# class ProfileForm(forms.ModelForm):
#     name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'name','class':'form-control', 'placeholder':'Enter User Full Name', 'disabled': True}))
#     profile_pic = forms.ImageField(required=True, widget=forms.FileInput(attrs={'id':'image', 'name':"picture", 'class':'form-control'}))

#     class Meta:
#         model = get_user_model()
#         fields = [
#             'name',
#             'picture'
#         ]


      
