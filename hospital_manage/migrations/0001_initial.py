# Generated by Django 3.2.16 on 2023-06-22 04:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admission_date', models.DateField()),
                ('discharge_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(choices=[('appointment', 'Appointment'), ('admission', 'Admission'), ('other', 'Other'), ('lab', 'Lab Services'), ('pharmacy', 'Pharmacy'), ('radiology', 'Radiology')], max_length=20)),
                ('billing_date', models.DateField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='department_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('specialization', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('image', models.ImageField(upload_to='doctor_images/')),
                ('available', models.BooleanField(default=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.department')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
                ('contact_number', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('image', models.ImageField(upload_to='patient_images/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admission_date', models.DateField()),
                ('discharge_date', models.DateField(blank=True, null=True)),
                ('diagnosis', models.TextField()),
                ('surgeries', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('prescription', models.TextField()),
                ('admission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.admission')),
                ('billing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.billing')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.patient')),
            ],
        ),
        migrations.AddField(
            model_name='billing',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.doctor'),
        ),
        migrations.AddField(
            model_name='billing',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.patient'),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('billing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.billing')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.patient')),
            ],
        ),
        migrations.AddField(
            model_name='admission',
            name='appointment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.appointment'),
        ),
        migrations.AddField(
            model_name='admission',
            name='billing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.billing'),
        ),
        migrations.AddField(
            model_name='admission',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.doctor'),
        ),
        migrations.AddField(
            model_name='admission',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.patient'),
        ),
        migrations.AddField(
            model_name='admission',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_manage.department'),
        ),
    ]
