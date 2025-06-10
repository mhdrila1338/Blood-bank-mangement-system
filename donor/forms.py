from django import forms
from django.contrib.auth.models import User
from . import models

class DonorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]
        widgets = {
            "password": forms.PasswordInput()
        }

class DonorForm(forms.ModelForm):
    class Meta:
        model = models.Donor
        fields = ['bloodgroup', 'mobile', 'profile_pic', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
