from django.db import models

class BloodStock(models.Model):
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

    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, unique=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.blood_group}: {self.quantity} units"
    
class BloodStock(models.Model):
    blood_group = models.CharField(max_length=5)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.blood_group}: {self.quantity} units"