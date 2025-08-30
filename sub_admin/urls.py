from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.subadmin_login_view, name='subadmin_login'),
    path('dashboard/', views.subadmin_dashboard, name='subadmin_dashboard'),

    # Donors & Patients
    path('donors/', views.donor_list, name='subadmin_donor_list'),
    path('patients/', views.patient_list_view, name='subadmin_patient_list'),
    path('patients/edit/<int:pk>/', views.patient_edit_view, name='subadmin_patient_edit'),
    path('patients/delete/<int:pk>/', views.patient_delete_view, name='subadmin_patient_delete'),

    # Blood Requests
    path('blood-requests/', views.subadmin_blood_requests, name='subadmin_blood_requests'),  # optional, or remove if unused
    path('requests/', views.blood_requests_view, name='blood_requests'),  # used for table display
    path('requests/approve/<int:request_id>/', views.approve_blood_request, name='approve_request'),
    path('requests/reject/<int:request_id>/', views.reject_blood_request, name='reject_blood_request'),

    # Blood Stock
    path('blood-stock/', views.available_blood_stock, name='subadmin_blood_stock'),

    # Donations
    path('donation-requests/', views.subadmin_donation_requests, name='subadmin_donation_requests'),
    path('donation-approve/<int:donation_id>/', views.approve_donation, name='approve_donation'),
    path('donation-reject/<int:donation_id>/', views.reject_donation, name='reject_donation'),
    path('pending-donations/', views.pending_donations_view, name='pending_donations'),
]
