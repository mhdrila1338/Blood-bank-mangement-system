from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from datetime import timedelta, date
from django.contrib.auth import logout
from sub_admin.views import home_view

from .models import Donor, Donation, UrgentRequest, HealthTip, Certificate
from .forms import DonorUserForm, DonorForm, ProfileUpdateForm, DonationForm

def donor_entry(request):
    return render(request,'donor/donor_entry.html')

# Signup View
def donor_signup_view(request):
    userform = DonorUserForm()
    donorForm = DonorForm()
    context = {'userform': userform, "donorForm": donorForm}

    if request.method == "POST":
        userform = DonorUserForm(request.POST)
        donorForm = DonorForm(request.POST, request.FILES)
        if userform.is_valid() and donorForm.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()

            donor = donorForm.save(commit=False)
            donor.user = user
            donor.bloodgroup = donorForm.cleaned_data['bloodgroup']
            donor.save()

            donor_group, created = Group.objects.get_or_create(name="DONOR")
            donor_group.user_set.add(user)

            return redirect('donor_login')
    return render(request, "donor/donor_signup.html", context=context)

# Login View
def donor_login_view(request):
    if request.method == 'POST':
        uname = request.POST.get("username")
        pwd = request.POST.get("password")
        user = authenticate(username=uname, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('afterlogin')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('donor_login')
    return render(request, "donor/donor_login.html")

# After login redirection
@login_required
def afterlogin_view(request):
    user = request.user
    if user.is_superuser:
        return redirect('subadmin_dashboard')
    elif hasattr(user, 'donor'):
        return redirect('donor_dashboard')
    elif hasattr(user, 'patient'):
        return redirect('patient_dashboard')
    else:
        return redirect('home_view')

# Dashboard
@login_required(login_url='donor_login')
def donor_dashboard_view(request):
    return render(request, 'donor/afterlogin.html')

# Donation stats
@login_required
def donation_stats(request):
    donations = Donation.objects.filter(donor=request.user).order_by('-created_at')
    total_donations = donations.count()
    return render(request, 'donor/donation_stats.html', {
        'donations': donations,
        'total_donations': total_donations
    })

# Urgent Requests
@login_required
def urgent_requests_view(request):
    donor = get_object_or_404(Donor, user=request.user)
    matching_requests = UrgentRequest.objects.filter(
        blood_group=donor.bloodgroup,
        status='Pending'
    ).order_by('-required_date')
    return render(request, 'donor/urgent_requests.html', {
        'urgent_requests': matching_requests
    })

# Health Tips
@login_required
def health_tips(request):
    tips = HealthTip.objects.all()
    return render(request, 'donor/health_tips.html', {'tips': tips})

# Update Profile
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('update_profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'donor/update_profile.html', {'form': form})

# Donate Blood
@login_required
def donate_blood_view(request):
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            return redirect('donor_dashboard')  # update this to your success URL
    else:
        form = DonationForm()

    today = date.today()
    next_eligible_date = today + timedelta(days=90)

    return render(request, 'donor/add_donation.html', {
        'form': form,
        'today': today,
        'next_eligible_date': next_eligible_date
    })

# Certificates
@login_required
def donor_certificates(request):
    donor = get_object_or_404(Donor, user=request.user)
    certificates = Certificate.objects.filter(donor=donor)
    return render(request, 'donor/certificates.html', {'certificates': certificates})

def donor_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been successfully logged out.")
    return redirect('donor_login')