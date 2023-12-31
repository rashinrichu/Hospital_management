# Generated by Django 3.2.16 on 2023-06-22 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_manage', '0003_remove_admission_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalrecord',
            name='ward',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.department'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='medicalrecord',
            name='diagnosis',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='medicalrecord',
            name='notes',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='medicalrecord',
            name='prescription',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='medicalrecord',
            name='surgeries',
            field=models.CharField(max_length=100),
        ),
    ]
