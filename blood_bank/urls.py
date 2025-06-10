from django.contrib import admin
from django.urls import path, include
from sub_admin.views import home_view
from donor.views import afterlogin_view  # import the afterlogin view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home_view, name='home'),

    path('admin/', admin.site.urls),

    # Subadmin URLs
    path('subadmin/', include('sub_admin.urls')),

    # Donor and Patient
    path('donor/', include('donor.urls')),
    path('patient/', include('patient.urls')),

    # Logout and After Login Handler
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('afterlogin/', afterlogin_view, name='afterlogin'),
]
