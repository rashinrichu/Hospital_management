from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')))
    contact_number = models.CharField(max_length=20)
    address = models.TextField()
    image = models.ImageField(upload_to='patient_images/')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='department_images/')

    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    specialization = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()
    image = models.ImageField(upload_to='doctor_images/')
    available = models.BooleanField(default=True)
    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"  
    
    
    
class Billing(models.Model):
    PAYMENT_CHOICES = [
        ('appointment', 'Appointment'),
        ('admission', 'Admission'),
        ('other', 'Other'),
        ('lab', 'Lab Services'),
        ('pharmacy', 'Pharmacy'),
        ('radiology', 'Radiology'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    billing_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    
    
    def __str__(self):
        return f"Billing for {self.patient} on {self.billing_date}"
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    def __str__(self):
        return f"Appointment for {self.patient} with {self.doctor} on {self.appointment_date}"
    
    
class Admission(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE)
    ward = models.ForeignKey(Department, on_delete=models.CASCADE) 


    def __str__(self):
        return f"Admission for {self.patient} in {self.ward}"
    
    

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE)
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE,null=True)
    ward = models.ForeignKey(Department, on_delete=models.CASCADE) 
    room=models.IntegerField(null=True,blank=True)
    admission_date = models.DateField()
    discharge_date = models.DateField(blank=True, null=True)
    diagnosis = models.CharField(max_length=100)
    surgeries = models.CharField(max_length=100)
    notes = models.CharField(max_length=100)
    prescription = models.CharField(max_length=100)

    def __str__(self):
        return f"Medical record for {self.patient} on {self.date}"
    
    
