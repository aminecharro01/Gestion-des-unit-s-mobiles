# Generated by Django 5.1.7 on 2025-05-25 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0006_alter_medicalstaff_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalstaff',
            name='user',
        ),
    ]
