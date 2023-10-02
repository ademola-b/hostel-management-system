from django import forms
from accounts.models import Department

class FilterForm(forms.Form):

    gender_choices = [
        ('male', 'male'),
        ('female', 'female')
    ]

    level_choices = [
    ('ND I', 'ND I'),
    ('ND II', 'ND II'),
    ('HND I', 'HND I'),
    ('HND II', 'HND II')
    ]

    payment_choices = [
        ('paid', 'paid'),
        ('unpaid', 'unpaid')
    ]

    gender = forms.ChoiceField(choices=gender_choices, label="Select Gender", widget=forms.Select(attrs={
        'class': 'form-control select form-select',
        'onchange': 'this.form.submit();'
    }))

    level = forms.ChoiceField(choices=level_choices, label="Select Level", widget=forms.Select(attrs={
        'class': 'form-control select form-select',
        'onchange': 'this.form.submit();'
    }))

    department = forms.ModelChoiceField(required=False, queryset=Department.objects.all(), empty_label="Select Department", widget=forms.Select(
        attrs={
            'class': 'form-control select form-select',
            'onchange': 'this.form.submit();'
        }
    ))

    payment = forms.ChoiceField(choices=payment_choices, widget=forms.Select(attrs={
        'class': 'form-control select form-select',
        'onchange': 'this.form.submit();'
    }))

    

    