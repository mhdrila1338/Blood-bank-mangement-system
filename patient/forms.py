from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import BloodRequest,Patient

# User Signup Form for Patients
class PatientUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

# Profile Information for Patients
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['profile_pic', 'age', 'blood_group', 'disease', 'doctorname', 'address', 'mobile']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Mobile Number'}),
        }

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['blood_group', 'quantity', 'reason']  # Use 'quantity' here, not 'units'
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={
                'min': 1,
                'class': 'form-control',
                'placeholder': 'Enter units needed',
            }),
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reason for blood request'}),
        }
