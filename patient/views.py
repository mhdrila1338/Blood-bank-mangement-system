from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import PatientUserForm, PatientForm, BloodRequestForm
from .models import BloodRequest, Patient
from sub_admin.models import BloodStock  # Adjust import path if needed


def patient_signup_view(request):
    if request.method == 'POST':
        userform = PatientUserForm(request.POST)
        patientform = PatientForm(request.POST, request.FILES)

        if userform.is_valid() and patientform.is_valid():
            user = userform.save()
            patient = patientform.save(commit=False)
            patient.user = user
            patient.save()
            login(request, user)
            return redirect('patient_login')  # update this to your actual dashboard URL name
    else:
        userform = PatientUserForm()
        patientform = PatientForm()

    context = {
        'userform': userform,
        'patientform': patientform,
    }
    return render(request, 'patient/signup.html', context)

def patient_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            user = authenticate(username=uname, password=pwd)
            if user is not None:
                login(request, user)
                return redirect('afterlogin')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'patient/login.html', {'form': form})



# ------------------ Patient Dashboard ------------------
@login_required(login_url='patient_login')
def patient_dashboard(request):
    return render(request, 'patient/dashboard.html')

# ------------------ List All Blood Requests ------------------
@login_required(login_url='patient_login')
def blood_request_list(request):
    patient = get_object_or_404(Patient, user=request.user)
    blood_requests = BloodRequest.objects.filter(patient=patient).order_by('-requested_at')
    total_requests = blood_requests.count()
    total_patients = 1  # For the patient, it’s always 1

    context = {
        'blood_requests': blood_requests,
        'total_requests': total_requests,
        'total_patients': total_patients,
    }
    return render(request, 'patient/blood_request_list.html', context)

# ------------------ Create Blood Request ------------------
@login_required(login_url='patient_login')
def blood_request_create(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            patient = get_object_or_404(Patient, user=request.user)
            blood_request.patient = patient
            blood_request.save()
            return redirect('patient_request_history')
    else:
        form = BloodRequestForm()
    return render(request, 'patient/blood_request_form.html', {'form': form})

# ------------------ Blood Request History ------------------
@login_required(login_url='patient_login')
def patient_request_history(request):
    patient = Patient.objects.get(user=request.user)
    requests = BloodRequest.objects.filter(patient=patient).order_by('-requested_at')
    context = {
        'blood_requests': requests,
    }
    return render(request, 'patient/request_history.html', context)

# ------------------ View Available Blood Stock ------------------
@login_required(login_url='patient_login')
def available_blood_stock(request):
    stocks = BloodStock.objects.all()
    return render(request, 'patient/blood_stock.html', {'stocks': stocks})


# ------------------ Notifications (placeholder) ------------------
@login_required(login_url='patient_login')
def notifications(request):
    notifications = []  # You can replace this with real notification logic
    return render(request, 'patient/notifications.html', {'notifications': notifications})


# ------------------ Profile Settings ------------------
@login_required(login_url='patient_login')
def profile_settings(request):
    return render(request, 'patient/profile_settings.html')


# ------------------ Contact Support ------------------
@login_required(login_url='patient_login')
def contact_support(request):
    return render(request, 'patient/contact_support.html')