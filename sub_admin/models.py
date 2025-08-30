from django.db import models

class BloodStock(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS, unique=True)
    units_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.blood_group} - {self.units_available} units"
    