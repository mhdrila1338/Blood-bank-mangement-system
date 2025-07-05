from django.db import models
from django.contrib.auth.models import User

# ------------------ Donor Model ------------------
class Donor(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('O+', 'O+'), ('O-', 'O-'),
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
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


# ------------------ Donation Model ------------------
BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('O+', 'O+'), ('O-', 'O-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
]

class Donation(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)  # ✅ ADD choices
    units = models.PositiveIntegerField()
    document = models.FileField(upload_to='donation_files/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.username} - {self.blood_group} - {self.units} units"


# ------------------ UrgentRequest Model ------------------
class UrgentRequest(models.Model):
    BLOOD_GROUP_CHOICES = Donor.BLOOD_GROUP_CHOICES
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, default='O+')
    contact_number = models.CharField(max_length=15, default='0000000000')
    reason = models.TextField(default='Not specified')
    hospital_name = models.CharField(max_length=200, default='Unknown Hospital')
    status = models.CharField(max_length=20, default='Pending')
    required_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient_name} - {self.blood_group}"


# ------------------ HealthTip Model ------------------
class HealthTip(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content[:30] + ("..." if len(self.content) > 30 else "")


# ------------------ Certificate Model ------------------
class Certificate(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='certificates/')

    def __str__(self):
        return self.title
