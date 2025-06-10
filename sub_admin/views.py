from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from donor.models import Donor
from patient.models import Patient, BloodRequest
from django.views.decorators.http import require_POST
from .models import BloodStock
from patient.forms import PatientForm  # already created 
# Home page
def home_view(request):
    return render(request, 'home_view.html')

# Subadmin login
def subadmin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('subadmin_dashboard')
            elif hasattr(user, 'donor'):
                messages.error(request, "Access Denied! Donors are not allowed to access the subadmin panel.")
            elif hasattr(user, 'patient'):
                messages.error(request, "Access Denied! Patients are not allowed to access the subadmin panel.")
            else:
                messages.error(request, "Access Denied! Unauthorized user.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'subadmin/login.html')

@login_required(login_url='subadmin_login')
def subadmin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access!")
        return redirect('subadmin_login')

    total_donors = Donor.objects.count()
    total_patients = Patient.objects.count()
    total_requests = BloodRequest.objects.count()
    blood_stock = BloodStock.objects.all()

    context = {
        'total_donors': total_donors,
        'total_patients': total_patients,
        'total_requests': total_requests,
        'blood_stock': blood_stock,
    }
    return render(request, 'subadmin/dashboard.html', context)

def is_subadmin(user):
    return user.is_superuser

@user_passes_test(is_subadmin, login_url='subadmin_login')
def donor_list(request):
    donors = Donor.objects.all()
    total_donors = donors.count()
    return render(request, "subadmin/donor_list.html", {
        "donors": donors,
        "total_donors": total_donors,
    })

def patient_list_view(request):
    patients = Patient.objects.all()
    return render(request, 'subadmin/patient_list.html', {'patients': patients})

@user_passes_test(is_subadmin, login_url='subadmin_login')
def subadmin_blood_requests(request):
    total_requests = BloodRequest.objects.count()
    total_patients = BloodRequest.objects.values('patient').distinct().count()
    blood_requests = BloodRequest.objects.all().order_by('-requested_at')
    context = {
        'total_requests': total_requests,
        'total_patients': total_patients,
        'blood_requests': blood_requests,
    }
    return render(request, 'subadmin/blood_request_list.html', context)

@user_passes_test(is_subadmin, login_url='subadmin_login')
def pending_requests(request):
    pending = BloodRequest.objects.filter(status='Pending').order_by('-requested_at')
    return render(request, 'subadmin/pending_requests.html', {'pending_requests': pending})

@user_passes_test(is_subadmin, login_url='subadmin_login')
@require_POST
def approve_request(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    if blood_request.status != "Approved":
        try:
            blood_stock = BloodStock.objects.get(blood_group=blood_request.blood_group)
        except BloodStock.DoesNotExist:
            messages.error(request, f"No stock found for blood group {blood_request.blood_group}.")
            return redirect('pending_requests')

        if blood_stock.quantity >= blood_request.quantity:
            blood_stock.quantity -= blood_request.quantity
            blood_stock.save()

            blood_request.status = "Approved"
            blood_request.save()
            messages.success(request, f'Request #{request_id} approved successfully.')
        else:
            messages.error(request, f"Insufficient stock for blood group {blood_request.blood_group}.")
    else:
        messages.info(request, f'Request #{request_id} is already approved.')

    return redirect('pending_requests')

def available_blood_stock(request):
    stocks = BloodStock.objects.all()
    return render(request, 'subadmin/available_blood_stock.html', {'stocks': stocks})
def patient_edit_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    if form.is_valid():
        form.save()
        return redirect('subadmin_patient_list')
    return render(request, 'subadmin/patient_edit.html', {'form': form})

def patient_delete_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    return redirect('subadmin_patient_list')
def blood_stock_view(request):
    dummy_stock = {
        'A+': 8,
        'A-': 3,
        'B+': 5,
        'B-': 2,
        'AB+': 4,
        'AB-': 1,
        'O+': 10,
        'O-': 2,
    }
    return render(request, 'sub_admin/blood_stock.html', {'blood_stock': dummy_stock})
# Note: The above code assumes that the necessary models and forms are already defined in the respective files.