# Generated by Django 5.2.1 on 2025-06-10 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0013_alter_bloodrequest_quantity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloodrequest',
            old_name='status',
            new_name='approved',
        ),
    ]
