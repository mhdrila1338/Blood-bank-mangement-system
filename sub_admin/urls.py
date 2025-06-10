from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.subadmin_login_view, name='subadmin_login'),
    path('dashboard/', views.subadmin_dashboard, name='subadmin_dashboard'),
    path('donors/', views.donor_list, name='subadmin_donor_list'),
     path('patients/', views.patient_list_view, name='subadmin_patient_list'),
    path('blood-requests/', views.subadmin_blood_requests, name='subadmin_blood_requests'),
    path('pending-requests/', views.pending_requests, name='pending_requests'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('blood-stock/', views.available_blood_stock, name='available_blood_stock'),
    path('patients/edit/<int:pk>/', views.patient_edit_view, name='subadmin_patient_edit'),
    path('patients/delete/<int:pk>/', views.patient_delete_view, name='subadmin_patient_delete'),
    path('blood-stock/', views.blood_stock_view, name='subadmin_blood_stock'),
]
