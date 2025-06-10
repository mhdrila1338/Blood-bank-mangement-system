from django.db import models
from django.contrib.auth.models import User
from django import forms

class Donor(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/donor', null=True, blank=True)
    bloodgroup = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    mobile = models.CharField(max_length=12)
    email = models.EmailField(null=True, blank=True)

    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    next_eligible_date = models.DateField()

    def __str__(self):
        return f"{self.donor.username} - {self.date}"

class UrgentRequest(models.Model):
    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=10)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.blood_group}"

class HealthTip(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content[:30] + ("..." if len(self.content) > 30 else "")

class Certificate(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='certificates/')

    def __str__(self):
        return self.title

# ProfileUpdateForm is better placed in forms.py, but if you want here:

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
