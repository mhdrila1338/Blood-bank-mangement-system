from django import forms
from django.contrib.auth.models import User
from .models import Donor, UrgentRequest, Donation

class DonorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]
        widgets = {
            "password": forms.PasswordInput()
        }

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['bloodgroup', 'mobile', 'profile_pic', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['blood_group', 'units', 'document']
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'units': forms.NumberInput(attrs={'class': 'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class UrgentRequestForm(forms.ModelForm):
    required_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    class Meta:
        model = UrgentRequest
        fields = ['patient_name', 'blood_group', 'contact_number', 'reason', 'hospital_name', 'required_date']
