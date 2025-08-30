from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.patient_signup_view, name='patient_signup'),
    path('login/', views.patient_login_view, name='patient_login'),
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient_logout/',views.patient_logout_view,name="patient_logout"),

    path('request-blood/', views.blood_request_create, name='blood_request_create'),
    path('blood-request/list/', views.blood_request_list, name='blood_request_list'),
    path('request-history/', views.patient_request_history, name='patient_request_history'),

    path('available-stock/', views.available_blood_stock, name='available_blood_stock'),
    path('notifications/', views.notifications, name='patient_notifications'),
    path('profile/', views.profile_settings, name='patient_profile_settings'),
    path('contact-support/', views.contact_support, name='patient_contact_support'),
    path('entry/',views.entry,name='entry_patient')
]

