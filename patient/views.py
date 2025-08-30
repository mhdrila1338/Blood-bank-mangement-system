from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.cache import never_cache

from .forms import PatientUserForm, PatientForm, BloodRequestForm
from .models import BloodRequest, Patient
from sub_admin.models import BloodStock
from django.contrib.auth.models import Group


def entry(request):
    return render(request, 'patient\patient_entry.html')


def patient_signup_view(request):
    if request.method == 'POST':
        user_form = PatientUserForm(request.POST)
        patient_form = PatientForm(request.POST, request.FILES)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            raw_password = user_form.cleaned_data.get('password1')
            user.set_password(raw_password)
            user.save()

            group = Group.objects.get(name='PATIENT')
            user.groups.add(group)

            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            return redirect('patient_login')
    else:
        user_form = PatientUserForm()
        patient_form = PatientForm()

    return render(request, 'patient/signup.html', {
        'user_form': user_form,
        'patient_form': patient_form
    })


def patient_login_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(username=uname, password=pwd)
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    if hasattr(user, 'patient') and user.patient is not None:
                        return redirect('patient_dashboard')
                    else:
                        logout(request)
                        messages.error(request, "You are not authorized as a patient.")
                        return redirect('patient_login')
                except Patient.DoesNotExist:
                    logout(request)
                    messages.error(request, "Patient profile does not exist.")
                    return redirect('patient_login')
            else:
                messages.error(request, "Your account is inactive.")
        else:
            messages.error(request, "Invalid login details.")
    return render(request, 'patient/login.html')


@never_cache
@login_required(login_url='patient_login')
def patient_dashboard(request):
    return render(request, 'patient/dashboard.html')


@never_cache
@login_required(login_url='patient_login')
def blood_request_list(request):
    patient = get_object_or_404(Patient, user=request.user)
    blood_requests = BloodRequest.objects.filter(patient=patient).order_by('-requested_at')
    total_requests = blood_requests.count()
    total_patients = 1
    context = {
        'blood_requests': blood_requests,
        'total_requests': total_requests,
        'total_patients': total_patients,
    }
    return render(request, 'patient/blood_request_list.html', context)


@never_cache
@login_required(login_url='patient_login')
def blood_request_create(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            patient = get_object_or_404(Patient, user=request.user)
            blood_request.patient = patient
            blood_request.status = 'Pending'
            blood_request.save()
            messages.success(request, "Blood request submitted successfully.")
            return redirect('patient_request_history')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BloodRequestForm()
    context = {'form': form}
    return render(request, 'patient/blood_request_form.html', context)


@never_cache
@login_required(login_url='patient_login')
def patient_request_history(request):
    patient = Patient.objects.get(user=request.user)
    requests = BloodRequest.objects.filter(patient=patient).order_by('-requested_at')
    context = {'blood_requests': requests}
    return render(request, 'patient/request_history.html', context)


@never_cache
@login_required(login_url='patient_login')
def available_blood_stock(request):
    stocks = BloodStock.objects.all()
    return render(request, 'subadmin/available_blood_stock.html', {'stocks': stocks})


@never_cache
@login_required(login_url='patient_login')
def notifications(request):
    notifications = []
    return render(request, 'patient/notifications.html', {'notifications': notifications})


@never_cache
@login_required(login_url='patient_login')
def profile_settings(request):
    return render(request, 'patient/profile_settings.html')


@never_cache
@login_required(login_url='patient_login')
def contact_support(request):
    return render(request, 'patient/contact_support.html')


def patient_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        request.session.flush()  # Clear session to prevent back access
        messages.success(request, "You have been successfully logged out.")
    return redirect('patient_login')

