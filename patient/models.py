from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='patient_profiles/', null=True, blank=True)
    age = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES)
    disease = models.CharField(max_length=100, blank=True)
    doctorname = models.CharField(max_length=100)
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('O+', 'O+'), ('O-', 'O-'),
    ('AB+', 'AB+'), ('AB-', 'AB-')
]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
]

class BloodRequest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    units = models.PositiveIntegerField()
    reason = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Request {self.id} by {self.patient.user.username}"