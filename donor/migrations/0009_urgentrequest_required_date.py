# Generated by Django 5.2.1 on 2025-06-12 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0008_alter_urgentrequest_hospital_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='urgentrequest',
            name='required_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
