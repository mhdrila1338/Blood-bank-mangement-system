from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from collections import defaultdict
from datetime import timedelta, date
from django.db.models import Sum

from patient.models import BloodRequest, Patient
from donor.models import Donor, Donation, UrgentRequest
from .models import BloodStock
from patient.forms import PatientForm

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
            elif hasattr(user, 'donor') or hasattr(user, 'patient'):
                messages.error(request, "Access Denied! Only subadmins can login here.")
            else:
                messages.error(request, "Access Denied! Unauthorized user.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'subadmin/login.html')

# Check if user is subadmin
def is_subadmin(user):
    return user.is_superuser

# Dashboard
@login_required(login_url='subadmin_login')
@user_passes_test(is_subadmin)
def subadmin_dashboard(request):
    context = {
        'total_donors': Donor.objects.count(),
        'total_patients': Patient.objects.count(),
        'total_requests': BloodRequest.objects.count(),
        'blood_stock': BloodStock.objects.all(),
        'pending_donations': Donation.objects.filter(status='Pending'),
    }
    return render(request, 'subadmin/dashboard.html', context)

# Donor list
@user_passes_test(is_subadmin, login_url='subadmin_login')
def donor_list(request):
    donors = Donor.objects.all()
    return render(request, "subadmin/donor_list.html", {"donors": donors})

# Patient list
@user_passes_test(is_subadmin, login_url='subadmin_login')
def patient_list_view(request):
    return render(request, 'subadmin/patient_list.html', {'patients': Patient.objects.all()})

# Edit & Delete Patient
@user_passes_test(is_subadmin, login_url='subadmin_login')
def patient_edit_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    if form.is_valid():
        form.save()
        return redirect('subadmin_patient_list')
    return render(request, 'subadmin/patient_edit.html', {'form': form})

@user_passes_test(is_subadmin, login_url='subadmin_login')
def patient_delete_view(request, pk):
    get_object_or_404(Patient, pk=pk).delete()
    return redirect('subadmin_patient_list')

# Blood Requests
@user_passes_test(is_subadmin, login_url='subadmin_login')
def subadmin_blood_requests(request):
    context = {
        'blood_requests': BloodRequest.objects.select_related('patient__user').all(),
        'urgent_requests': UrgentRequest.objects.select_related('user').all(),
    }
    return render(request, 'subadmin/blood_requests.html', context)

@user_passes_test(is_subadmin, login_url='subadmin_login')
def approve_blood_request(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)

    if blood_request.status != 'Pending':
        messages.warning(request, 'This request is already processed.')
        return redirect('subadmin_blood_requests')

    try:
        stock = BloodStock.objects.get(blood_group=blood_request.blood_group)
    except BloodStock.DoesNotExist:
        messages.error(request, 'Blood group not found in stock.')
        return redirect('subadmin_blood_requests')

    if stock.units_available >= blood_request.units:
        stock.units_available -= blood_request.units
        stock.save()

        blood_request.status = 'Approved'
        blood_request.save()  # 🔥 IMPORTANT: Make sure this is here
        messages.success(request, f'Request approved and {blood_request.units} unit(s) deducted from stock.')
    else:
        messages.error(request, f'Not enough stock to approve the request. Only {stock.units_available} unit(s) available.')

    return redirect('subadmin_blood_requests')

@user_passes_test(is_subadmin, login_url='subadmin_login')
def reject_blood_request(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    if blood_request.status == "Pending":
        blood_request.status = "Rejected"
        blood_request.save()
        messages.warning(request, "Request rejected.")
    else:
        messages.info(request, "Already processed.")
    return redirect('subadmin_blood_requests')



def blood_requests_view(request):
    from patient.models import BloodRequest
    blood_requests = BloodRequest.objects.all().order_by('-requested_at')  # Fresh every time
    return render(request, 'subadmin/blood_requests.html', {'blood_requests': blood_requests})



# Blood Stock View (Dynamic)
@user_passes_test(is_subadmin, login_url='subadmin_login')
def available_blood_stock(request):
    from .models import BloodStock  # ensure you're using the correct model

    # Initialize all blood groups with 0
    stock = {bg[0]: 0 for bg in BloodStock.BLOOD_GROUPS}

    # Update actual available units from DB
    for entry in BloodStock.objects.all():
        stock[entry.blood_group] = entry.units_available

    return render(request, 'subadmin/blood_stock.html', {'stock': stock})

# Donation Requests
@login_required
def subadmin_donation_requests(request):
    donations = Donation.objects.all().order_by('-created_at')
    return render(request, 'subadmin/donation_requests.html', {'donations': donations})

@login_required
def approve_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    donation.status = 'Approved'    
    donation.save()
    stock, _ = BloodStock.objects.get_or_create(blood_group=donation.blood_group)
    stock.units_available += donation.units
    stock.save()
    return redirect('subadmin_donation_requests')

@login_required
def reject_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    donation.status = 'Rejected'
    donation.save()
    messages.warning(request, 'Donation rejected.')
    return redirect('subadmin_donation_requests')

@login_required
def pending_donations_view(request):
    return render(request, 'subadmin/donation_requests.html', {
        'donations': Donation.objects.filter(status='Pending')
    })
