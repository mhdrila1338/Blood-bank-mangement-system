from django.urls import path
from . import views

urlpatterns = [
    path('donor/signup/', views.donor_signup_view, name='donor_signup'),
    path('donor/login/', views.donor_login_view, name='donor_login'),
    path('donor/dashboard/', views.donor_dashboard_view, name='donor_dashboard'),
    path('afterlogin/', views.afterlogin_view, name='afterlogin'),
    path('add-donation/', views.add_donation, name='add_donation'),
    path('next-donation-date/', views.next_donation_date, name='next_donation_date'),
    path('donation-stats/', views.donation_stats, name='donation_stats'),
    path('urgent-requests/', views.urgent_requests, name='urgent_requests'),
    path('health-tips/', views.health_tips, name='health_tips'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('certificates/', views.certificates, name='certificates'),
]
