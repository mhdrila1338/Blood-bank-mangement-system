# Generated by Django 5.2.1 on 2025-06-05 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_admin', '0003_bloodrequests_contact_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodrequests',
            name='blood_group',
            field=models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3),
        ),
    ]
