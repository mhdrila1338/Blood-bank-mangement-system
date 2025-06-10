from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from . import forms
from .models import Donation, UrgentRequest, HealthTip, Certificate
from .forms import ProfileUpdateForm

# Donor Signup View
def donor_signup_view(request):
    userform = forms.DonorUserForm()
    donorForm = forms.DonorForm()
    context = {'userform': userform, "donorForm": donorForm}

    if request.method == "POST":
        userform = forms.DonorUserForm(request.POST)
        donorForm = forms.DonorForm(request.POST, request.FILES)
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

# Donor Login View
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

# Donor Dashboard
@login_required(login_url='donor_login')
def donor_dashboard_view(request):
    return render(request, 'donor/afterlogin.html')

# Role-based Redirection after Login
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

# Show latest donation and next eligible donation date
@login_required
def next_donation_date(request):
    latest_donation = Donation.objects.filter(donor=request.user).order_by('-date').first()
    return render(request, 'donor/next_donation_date.html', {'latest_donation': latest_donation})

# View donation stats for logged-in donor
@login_required
def donation_stats(request):
    donations = Donation.objects.filter(donor=request.user).order_by('-date')
    total_donations = donations.count()
    return render(request, 'donor/donation_stats.html', {
        'donations': donations,
        'total_donations': total_donations
    })

# Show urgent blood requests
@login_required
def urgent_requests(request):
    requests = UrgentRequest.objects.all().order_by('-created_at')
    return render(request, 'donor/urgent_requests.html', {'requests': requests})

# Show health tips
@login_required
def health_tips(request):
    tips = HealthTip.objects.all()
    return render(request, 'donor/health_tips.html', {'tips': tips})

# Update donor profile
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

# Show donor certificates
@login_required
def certificates(request):
    certificates = Certificate.objects.filter(donor=request.user)
    return render(request, 'donor/certificates.html', {'certificates': certificates})

# Add donation page - add login protection
@login_required
def add_donation(request):
    return render(request, 'donor/add_donation.html')
