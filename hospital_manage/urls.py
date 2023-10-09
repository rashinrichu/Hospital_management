from django.contrib import admin
from django.urls import path,include
from hospital_manage import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about_us/',views.about_us,name='about_us'),
    path('Insurance/',views.Insurance,name='Insurance'),
    path('contact/',views.contact,name='contact'),
    path('department/',views.department,name='department'),
    path('booknow/',views.booknow,name='booknow'),
    path('cardiology/',views.cardiology,name='cardiology'),
    path('neurology/',views.neurology,name='neurology'),
    path('ortho/',views.ortho,name='ortho'),
    path('register/',views.register,name='register'),
    path('registration_patient/',views.registration_patient,name='registration_patient'),
    path('user_login/',views.user_login,name='user_login'),
    path('patients_home/',views.patients_home,name='patients_home'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('logout/',views.logout,name='logout'),
    path('patient_profile/',views.patient_profile,name='patient_profile'),
    path('edit_patient_profile/<int:patient_id>/', views.edit_patient_profile, name='edit_patient_profile'),    path('add_department/',views.add_department,name='add_department'),
    path('department_list/',views.department_list,name='department_list'),
    path('edit_department/<int:department_id>/',views.edit_department,name='edit_department'),
    path('add_doctor/',views.add_doctor,name='add_doctor'),
    path('edit_doctor/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('view_all_doctors/',views.view_all_doctors,name='view_all_doctors'),
    path('create_appointment/',views.create_appointment,name='create_appointment'),
    path('appointment_list/',views.appointment_list,name='appointment_list'),
    path('appointment_list_admin/',views.appointment_list_admin,name='appointment_list_admin'),
    path('add_admission/',views.add_admission,name='add_admission'),
    path('add_medical_record/',views.add_medical_record,name='add_medical_record'),
    path('create_billing/',views.create_billing,name='create_billing'),
    path('billing_detail/',views.billing_detail,name='billing_detail'),
    path('all_medical_records/',views.all_medical_records,name='all_medical_records'),
    path('edit_medical_record/<int:record_id>/', views.edit_medical_record, name='edit_medical_record'),
    path('search/',views.search,name='search'),
    path('view_all_doctors_patient/',views.view_all_doctors_patient,name='view_all_doctors_patient'),

    path('all_admissions/',views.all_admissions,name='all_admissions'),
    path('patients_view/',views.patients_view,name='patients_view'),
    path('delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('search_for_admin/',views.search_for_admin,name='search_for_admin'),
    path('department_list_patient/',views.department_list_patient,name='department_list_patient'),
    path('delete_medical_record/<int:record_id>/',views.delete_medical_record,name='delete_medical_record'),

    path('delete_admission_record/<int:admission_id>/', views.delete_admission_record, name='delete_admission_record'),
    path('all_medical_records_patient/',views.all_medical_records_patient,name='all_medical_records_patient'),
    path('delete_department/<int:department_id>/',views.delete_department,name='delete_department'),












]
