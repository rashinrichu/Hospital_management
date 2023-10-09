from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required


from django.conf import settings
from .models import Patient, Department, Doctor, Admission, Billing, MedicalRecord, Appointment
from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from .models import Department

# Create your views here.
def index(request):
    return render(request,'index.html')


def about_us(request):
    return render(request,'about us.html')


def Insurance(request):
    return render(request,'insurance.html')

def contact(request):
    return render(request,'contact.html')

def department(request):
    return render(request,'department.html')

def booknow(request):
    return render(request,'booknow.html')

def cardiology(request):
    return render(request,'cardiology.html')

def neurology(request):
    return render(request,'neurology.html')

def ortho(request):
  
    return render(request,'ortho.html')

def register(request):
    return render(request,'register.html')

def patients_home(request):
    return render(request,'patients_home.html')

def admin_home(request):
    return render(request,'admin_home.html')





def registration_patient(request):
    default_image = settings.STATIC_URL + 'static/img/User.png'

    if request.method == 'POST':
        # Get the user data from the request
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        image = request.FILES.get('image')

        # Check if the passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('index')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('index')

        # Create the user object
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)

        # Create the patient object
        if not image:  # If no image is uploaded, set a default image path
            patient = Patient.objects.create(user=user, date_of_birth=date_of_birth, gender=gender, contact_number=phone_number, address=address, image=default_image)
        else:
            patient = Patient.objects.create(user=user, date_of_birth=date_of_birth, gender=gender, contact_number=phone_number, address=address, image=image)

        # Send a confirmation email to the user
        subject = 'Welcome to Medical Clinic'
        message = f'Thank you for joining our hospital! Your registration as a patient was successful. We look forward to serving you.\n\nYour username: {username}\nYour password: {password}'        
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        # Redirect to the index page with a success message
        messages.success(request, 'Registration successful. Please log in to access your account.')
        return redirect('index')
    else:
        context = {'default_image': default_image}
        return render(request, 'index.html', context)
    
    
    





#login


def user_login(request):
    alert = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Logged in successfully!')
            if user.is_staff:
                return redirect('admin_home')
            else:
                return redirect('patients_home')
        else:
            messages.error(request, 'Invalid username or password')
            alert = True
    return render(request, 'index.html', {'alert': alert})



def logout(request):
	auth.logout(request)
	return redirect('index')


#patients_profile



def patient_profile(request):
    try:
        patient = Patient.objects.get(user=request.user)
        context = {'patient': patient}
        return render(request, 'patient_profile.html', context)
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile does not exist')
        return redirect('index')
    
   #edit profile 
    
def edit_patient_profile(request, patient_id):
    if request.user.is_authenticated:
        try:
            patient = Patient.objects.get(user=request.user, id=patient_id)
            if request.method == 'POST':
                # Retrieve updated data from the form
                patient.user.first_name = request.POST.get('first_name')
                patient.user.last_name = request.POST.get('last_name')
                patient.user.email = request.POST.get('email')
                patient.gender = request.POST.get('gender')
                patient.contact_number = request.POST.get('contact_number')
                patient.address = request.POST.get('address')
                image = request.FILES.get('image')
                if image:
                    patient.image = image
                # Check if the date of birth field is provided
                if request.POST.get('date_of_birth'):
                    patient.date_of_birth = request.POST.get('date_of_birth')
                # Save the updated patient profile and user information
                patient.user.save()
                patient.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('patient_profile')

            context = {'patient': patient}
            return render(request, 'edit_patient_profile.html', context)
        except Patient.DoesNotExist:
            messages.error(request, 'Patient profile does not exist')
    return redirect('index')  # Redirect to the homepage or display an error message


#add department

def add_department(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES.get('image')
        department = Department(name=name, description=description, image=image)
        department.save()
        messages.success(request, 'Department added successfully.')
        return redirect('department_list')
    return render(request, 'add_department.html')
#edit department
def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        department.name = request.POST['name']
        department.description = request.POST['description']
        image = request.FILES.get('image')
        if image:
            department.image = image
        department.save()
        messages.success(request, 'Department updated successfully.')

        return redirect('department_list')
    context = {'department': department}
    return render(request, 'department.html', context)

#show all department 
def department_list(request):
    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, 'department.html', context)

def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    department.delete()
    messages.success(request, 'Department deleted successfully.')
    return redirect('department_list')

def department_list_patient(request):
    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, 'department_list.html', context)


from django.shortcuts import render, redirect
from .models import Department, Doctor

def add_doctor(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        specialization = request.POST['specialization']
        department_id = request.POST['department']
        contact_number = request.POST['contact_number']
        address = request.POST['address']
        image = request.FILES.get('image')

        department = Department.objects.get(id=department_id)
        doctor = Doctor(
            first_name=first_name,
            last_name=last_name,
            email=email,
            specialization=specialization,
            department=department,
            contact_number=contact_number,
            address=address,
            image=image
        )
        doctor.save()
        messages.success(request, 'Doctor added successfully.')

        return redirect('view_all_doctors')

    departments = Department.objects.all()
    return render(request, 'add_doctor.html', {'departments': departments})

#edit doctor

from django.shortcuts import get_object_or_404

def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        doctor.first_name = request.POST['first_name']
        doctor.last_name = request.POST['last_name']
        doctor.email = request.POST['email']
        doctor.specialization = request.POST['specialization']
        doctor.department_id = request.POST['department']
        doctor.contact_number = request.POST['contact_number']
        doctor.address = request.POST['address']
        if 'image' in request.FILES:
            doctor.image = request.FILES['image']
        
        doctor.available = request.POST.get('availability') == 'True'
        doctor.save()
        messages.success(request, 'Doctor updated successfully.')

        return redirect('view_all_doctors')
    
    departments = Department.objects.all()
    return render(request, 'edit_doctor.html', {'doctor': doctor, 'departments': departments})

#view doctors
def view_all_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'view_all_doctors.html', {'doctors': doctors})

#create appointment

from datetime import datetime, date

from django.contrib.auth.decorators import login_required

@login_required

def create_appointment(request):
    PAYMENT_CHOICES = [
        ('appointment', 'Appointment'),
        ('admission', 'Admission'),
        ('other', 'Other'),
        ('lab', 'Lab Services'),
        ('pharmacy', 'Pharmacy'),
        ('radiology', 'Radiology'),
    ]

    booking_limit = 4

    if request.method == 'POST':
        appointment_date = datetime.strptime(request.POST['appointment_date'], '%Y-%m-%d').date()
        today = date.today()

        if appointment_date == today:
            # Check the total number of appointments made today
            appointment_count = Appointment.objects.filter(appointment_date=today).count()

            if appointment_count >= booking_limit:
                messages.error(request, 'Booking limit exceeded. No more appointments available for today.')
                return redirect('create_appointment')

        patient = get_object_or_404(Patient, user=request.user)
        doctor_id = request.POST['doctor_id']

        # Check if the user already has an appointment with the selected doctor on the same day
        existing_appointment = Appointment.objects.filter(patient=patient, doctor_id=doctor_id, appointment_date=appointment_date).exists()
        if existing_appointment:
            messages.error(request, 'You have already booked an appointment with this doctor on the same day.')
            return redirect('create_appointment')

        appointment_time = request.POST['appointment_time']
        payment_type = request.POST['payment_type']
        amount = request.POST['amount']

        # Get the doctor object
        doctor = get_object_or_404(Doctor, id=doctor_id)

        # Create the billing object
        billing_date = today  # Set the billing date to the current date
        billing = Billing.objects.create(
            patient=patient,
            doctor=doctor,
            payment_type=payment_type,
            billing_date=billing_date,
            amount=amount
        )

        # Create the appointment object
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            billing=billing,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )
        messages.success(request, 'Appointment created successfully.')
        return redirect('appointment_list')

    doctors = Doctor.objects.all()

    context = {
        'payment_choices': PAYMENT_CHOICES,
        'doctors': doctors,
        'booking_limit': booking_limit,
        'billing_date': date.today(),
    }
    return render(request, 'create_appointment.html', context)
#list of appointment patients
def appointment_list(request):
    user = request.user
    today = date.today()
    appointments = Appointment.objects.filter(patient__user=user, appointment_date__gte=today).select_related('billing')
    context = {
        'appointments': appointments
    }
    return render(request, 'appointment_list.html', context)

from django.contrib.admin.views.decorators import staff_member_required
#list of all appointment admin
@staff_member_required
def appointment_list_admin(request):
    current_date = date.today()
    appointments = Appointment.objects.select_related('billing').filter(appointment_date__gte=current_date)
    context = {
        'appointments': appointments
    }
    return render(request, 'appointment_list_admin.html', context)



#add admission
def add_admission(request):
    if request.method == 'POST':
        patient_id = request.POST['patient']
        doctor_id = request.POST['doctor']
        billing_id = request.POST['billing']
        ward_id = request.POST['ward']

        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)
        billing = Billing.objects.get(id=billing_id)
        ward = Department.objects.get(id=ward_id)

        admission = Admission(
            patient=patient,
            doctor=doctor,
            billing=billing,
            ward=ward,
        )
        admission.save()
        return redirect('all_admissions')

    # Fetch the necessary data to populate the form fields
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    billings = Billing.objects.all()
    wards = Department.objects.all()

    context = {
        'patients': patients,
        'doctors': doctors,
        'billings': billings,
        'wards': wards
    }

    return render(request, 'add_admission.html', context)

def all_admissions(request):
    admissions = MedicalRecord.objects.select_related('patient', 'doctor', 'billing', 'ward').all()

    context = {
        'admissions': admissions,
    }

    return render(request, 'all_admissions.html', context)

from django.utils.datastructures import MultiValueDictKeyError


#patient record view 

#add medical record
def add_medical_record(request):
    if request.method == 'POST':
        # Retrieve the form data
        patient_id = request.POST['patient']
        doctor_id = request.POST['doctor']
        billing_id = request.POST['billing']
        ward_id = request.POST['ward']
        admission_date = request.POST['admission_date']
        discharge_date = request.POST.get('discharge_date')
        diagnosis = request.POST['diagnosis']
        surgeries = request.POST['surgeries']
        notes = request.POST['notes']
        prescription = request.POST['prescription']
        room = request.POST.get('room')

        patient = Patient.objects.get(pk=patient_id)
        doctor = Doctor.objects.get(pk=doctor_id)
        billing = Billing.objects.get(pk=billing_id)
        ward = Department.objects.get(pk=ward_id)

        try:
            admission_id = request.POST['admission']
            admission = Admission.objects.get(pk=admission_id)
        except MultiValueDictKeyError:
            admission = None

        medical_record = MedicalRecord(
            patient=patient,
            doctor=doctor,
            billing=billing,
            admission=admission,
            ward=ward,
            room=room,
            admission_date=admission_date,
            discharge_date=discharge_date,
            diagnosis=diagnosis,
            surgeries=surgeries,
            notes=notes,
            prescription=prescription
        )
        medical_record.save()
        messages.success(request, 'Record added successfully.')

        return redirect('all_medical_records')

    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    billings = Billing.objects.all()
    wards = Department.objects.all()
    admissions = Admission.objects.all()

    context = {
        'patients': patients,
        'doctors': doctors,
        'billings': billings,
        'wards': wards,
        'admissions': admissions,
    }

    return render(request, 'add_medical_record.html', context)


def edit_medical_record(request, record_id=None):
    if record_id:
        # Retrieve the existing medical record
        medical_record = get_object_or_404(MedicalRecord, pk=record_id)
    else:
        medical_record = None

    if request.method == 'POST':
        # Retrieve the form data
        patient_id = request.POST['patient']
        doctor_id = request.POST['doctor']
        billing_id = request.POST['billing']
        ward_id = request.POST['ward']
        admission_date = request.POST['admission_date']
        discharge_date = request.POST.get('discharge_date')
        diagnosis = request.POST['diagnosis']
        surgeries = request.POST['surgeries']
        notes = request.POST['notes']
        prescription = request.POST['prescription']
        room= request.POST['room']


        # Update the medical record object with the new data
        medical_record.patient_id = patient_id
        medical_record.doctor_id = doctor_id
        medical_record.billing_id = billing_id
        medical_record.ward_id = ward_id
        medical_record.admission_date = admission_date
        medical_record.discharge_date = discharge_date
        medical_record.diagnosis = diagnosis
        medical_record.surgeries = surgeries
        medical_record.notes = notes
        medical_record.prescription = prescription
        medical_record.room = room

        medical_record.save()
        messages.success(request, 'Record updated successfully.')

        return redirect('all_medical_records')

    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    billings = Billing.objects.all()
    wards = Department.objects.all()

    context = {
        'patients': patients,
        'doctors': doctors,
        'billings': billings,
        'wards': wards,
        'medical_record': medical_record
    }

    return render(request, 'edit_medical_record.html', context)



def all_medical_records(request):
    today = date.today()
    records = MedicalRecord.objects.all().order_by('-admission_date')
    context = {'records': records, 'today': today}
    return render(request, 'all_medical_records.html', context)
#patients view
def all_medical_records_patient(request):
    user = request.user
    patient = Patient.objects.get(user=user)
    records = MedicalRecord.objects.filter(patient=patient)
    context = {'records': records}
    return render(request, 'all_medical_records_patient.html', context)

#admission

def create_billing(request):
    if request.method == 'POST':
        # Retrieve the logged-in user
        user = request.user

        # Retrieve the form data
        doctor_id = request.POST['doctor']
        payment_type = request.POST['payment_type']
        amount = request.POST['amount']

        # Retrieve the patient based on the logged-in user
        patient = get_object_or_404(Patient, user=user)

        # Retrieve the doctor
        doctor = get_object_or_404(Doctor, id=doctor_id)

        # Create the billing object
        billing = Billing.objects.create(
            patient=patient,
            doctor=doctor,
            payment_type=payment_type,
            amount=amount
        )
        messages.success(request, 'Bill Paid successfully.')  # Add success message
        return redirect('billing_detail')

    # Retrieve the patients based on the logged-in user
    patients = Patient.objects.filter(user=request.user)
    doctors = Doctor.objects.all()

    context = {
        'patients': patients,
        'doctors': doctors,
        'payment_choices': Billing.PAYMENT_CHOICES
    }

    return render(request, 'create_billing.html', context)


def billing_detail(request):
    user = request.user
    billing = Billing.objects.filter(patient__user=user).prefetch_related('doctor')
    context = {
        'billing': billing
    }
    return render(request, 'billing_detail.html', context)


def search(request):
    query = request.GET.get('q')

    departments = Department.objects.filter(name__icontains=query)
    doctors = Doctor.objects.filter(first_name__icontains=query) | Doctor.objects.filter(last_name__icontains=query)

    context = {
        'departments': departments,
        'doctors': doctors,
        'query': query
    }

    return render(request, 'search.html', context)

#patients view
def view_all_doctors_patient(request):
    doctors = Doctor.objects.all()
    return render(request, 'view_all_doctors_patient.html', {'doctors': doctors})


def patients_view(request):
    # Retrieve all patients
    patients = Patient.objects.all()

    context = {
        'patients': patients
    }

    return render(request, 'patients.html', context)



def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        # Delete the patient
        patient.delete()
        return redirect('patients_view')  # Redirect to a page displaying the list of patients
    
    return render(request, 'patients.html', {'patient': patient})



def search_for_admin(request):
    query = request.GET.get('q')

    departments = Department.objects.filter(name__icontains=query)
    doctors = Doctor.objects.filter(first_name__icontains=query) | Doctor.objects.filter(last_name__icontains=query)

    context = {
        'departments': departments,
        'doctors': doctors,
        'query': query
    }

    return render(request, 'search_admin.html', context)


#delete record 

def delete_medical_record(request, record_id):
    medical_record = get_object_or_404(MedicalRecord, pk=record_id)

    if request.method == 'POST':
        medical_record.delete()
        return redirect('all_medical_records')

    context = {
        'medical_record': medical_record
    }

    return render(request, 'all_medical_record.html', context)



def delete_admission_record(request,admission_id):
    admission_record = get_object_or_404(Admission, pk=admission_id)

    if request.method == 'POST':
        admission_record.delete()
        return redirect('all_admissions')

    context = {
        'admission': admission_record   
        }

    return render(request, 'all_admission.html', context)