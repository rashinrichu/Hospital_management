# Generated by Django 3.2.16 on 2023-06-22 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_manage', '0002_admission_room_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admission',
            name='appointment',
        ),
    ]