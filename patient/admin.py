from django.contrib import admin
from .models import Patient,BloodRequest # ✅ Correct import

admin.site.register(Patient)
admin.site.register(BloodRequest)