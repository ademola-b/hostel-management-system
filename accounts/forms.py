import datetime
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model, validators
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone

from .models import Student, Department, School, StudentContact

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'id': 'exampleInputEmail1','class':'form-control form-control-lg', 'placeholder':'Matriculation Number/Username', 'autofocus': 'true'}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'id':'exampleInputPassword1','class':'form-control form-control-lg', 'placeholder':'Password'}))


class SignUpForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your registration number'}),
                               )
    email = forms.EmailField(required=True, max_length=254, help_text='Enter a valid email address', widget=forms.EmailInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder':'Enter your Email Address'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder':'Enter Password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder':'Confirm Password'}))

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

    bloodgroup_choices = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your first name'}))
    middle_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your middle name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your last name'}))
    email = forms.EmailField(required=False, max_length=254, help_text='Enter a valid email address', widget=forms.EmailInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder':'Enter your Email Address', 'disabled':'disabled'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your phone number'}))
    
    dob = forms.DateField(required=True, widget = forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))

    blood_group = forms.ChoiceField(required=True, choices=bloodgroup_choices, widget=forms.Select(
        attrs={
            'class': 'form-control select form-select'
        }))
    
    gender = forms.ChoiceField(required=True, choices=gender_choices, widget=forms.Select(attrs={
        'class': 'form-control select form-select'
    }))

    profile_pic = forms.ImageField(
        required=True, help_text="Student Picture", widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'type': 'file',
                'accept': 'image/jpeg, image/png'
            }))
    

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "dob",
            "blood_group",
            "profile_pic",
            "phone",
            "gender"
        ]
    
    def __init__(self, request, *args, **kwargs):
        super(UserUpdateProfileForm, self).__init__(*args, **kwargs)

        self.fields['email'].initial = request.user.email

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        print(dob)
        if dob and dob > timezone.now().date():
            raise forms.ValidationError("Date cannot be a future date")
        return dob

class StudentProfileForm(forms.ModelForm):

    level_choice = [
    ('ND I', 'ND I'),
    ('ND II', 'ND II'),
    ('HND I', 'HND I'),
    ('HND II', 'HND II'),
    ('ND II SPILLOVER', 'ND II SPILLOVER'),
    ('HND II SPILLOVER', 'HND II SPILLOVER'),
    ]

    school = forms.ModelChoiceField(required=True, queryset=School.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control select form-select',
            # 'onchange': 'this.form.submit()'
        }
    ))

    department = forms.ModelChoiceField(queryset=Department.objects.none(), widget=forms.Select(
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
            "school",
            "department",
            "level"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.none()

        print(f"data: {self.data}")
        if 'school' in self.data:
            try:
                school_id = str(self.data.get('school'))
                print(f"scc: {school_id}")
                self.fields['department'].queryset = Department.objects.filter(school__school_id = school_id)
            except:
                pass
        elif self.instance and self.instance.school:
            # pass
            # print(type(self.instance.department))
            # print(f"in: {self.instance.pk}")
            self.fields['department'].queryset = self.instance.school.department_set

class StudentContactForm(forms.ModelForm):

    address = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter your address'}))
    parent_phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter parent/guardian phone'}))
    parent_address = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter parent/guardian address'}))
    next_of_kin_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter next of kin name'}))
    next_of_kin_phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter next of kin phone'}))
    next_of_kin_address = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter next of kin address'}))
    
    class Meta:
        model = StudentContact
        fields = [
            "address",
            "parent_phone",
            "parent_address",
            "next_of_kin_name", 
            "next_of_kin_phone",
            "next_of_kin_address"
        ]
 
