from django.contrib import admin
from .models import Patient, Department, Doctor, Admission, Billing, MedicalRecord, Appointment

admin.site.register(Patient)
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Admission)
admin.site.register(Billing)
admin.site.register(MedicalRecord)
admin.site.register(Appointment)


