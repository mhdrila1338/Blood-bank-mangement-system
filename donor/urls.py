from django.urls import path
from . import views


urlpatterns = [
    path('donor/donor_entry',views.donor_entry,name='donor_entry'),
    path('donor/signup/', views.donor_signup_view, name='donor_signup'),
    path('login/', views.donor_login_view, name='donor_login'),
    path('donor/dashboard/', views.donor_dashboard_view, name='donor_dashboard'),
    path('afterlogin/', views.afterlogin_view, name='afterlogin'),
    path('logou/',views.donor_logout_view,name='donor_logout'),
    # Corrected function name here 👇
    path('add-donation/', views.donate_blood_view, name='add_donation'),
    path('donation-stats/', views.donation_stats, name='donation_stats'),
    path('urgent-requests/', views.urgent_requests_view, name='urgent_requests'),
    path('health-tips/', views.health_tips, name='health_tips'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('certificates/', views.donor_certificates, name='donor_certificates'),
    path('donate-blood/', views.donate_blood_view, name='donate_blood'),
]
