from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from .decoators import *
from .functions import *

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

    
#=========================================================================================
#=============================REGISTER AND LOGIN FOR USERS ===============================
#=========================================================================================
   

@unauthenticated_user
def patient_register_page(request):
    
    form      = Register()
    
    name_form = PatientRegister()
    
    if request.method =='POST' :
        form      = Register(request.POST)
        
        name_form = PatientRegister(request.POST)
        
        if form.is_valid() and name_form.is_valid():
            user    = form.save()
            
            patient = name_form.save(commit=False)
            
            group   = Group.objects.get(name='patient')
            # Add the user role in the groups
            
            user.groups.add(group)
            patient.user = user
            patient.save()
            messages.success(request, f"Account created for {form.cleaned_data.get('username')}")
            return redirect('login')
            
    context = {'form' :form,
               'name_form':name_form}
    return render(request, 'register_patient.html', context)


@unauthenticated_user
def employee_register_page(request):
    
    form        = Register()
    
    clinic_form = EmployeeRegister()
    
    if request.method=='POST' :
        
        form        = Register(request.POST)
        
        clinic_form = EmployeeRegister(request.POST)
        
        if form.is_valid() and clinic_form.is_valid():
            
            user          = form.save()
            
            employee      = clinic_form.save(commit=False)
            
            group,created = Group.objects.get_or_create(name='employee')
            
            employee.user = user
            
            user.groups.add(group)
            employee.save()
            messages.success(request, f"Account created for {form.cleaned_data.get('username')}")
            return redirect('login')
            
    context = {'form' :form,
               'clinic_form':clinic_form}
    
    return render(request, 'register_employee.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        
        login_id = request.POST.get('login_id')  # Can be username or email
        
        password = request.POST.get('password')
        
        User = get_user_model()
        
        user = User.objects.filter(Q(username=login_id) | Q(email=login_id)).first()
        
        if user is not None and user.check_password(password):
            login(request, user)
            return redirect('home')
        else: 
            messages.info(request, 'Username or Email or Password is incorrect')
            
    context = {}
    return render(request, 'login.html', context)

@unauthenticated_user
def forgot_password(request):
    temp_password = None
    if request.method == 'POST':
        
        email = request.POST['email']
        
        user  = User.objects.filter(email=email).first()
        
        if user:
            
            temp_password = generate_temp_password()
            
            user.set_password(temp_password)
            user.save()
    return render(request, 'forgot_password.html', {'temp_password': temp_password})

def logout_user(request):
    logout(request)
    return redirect('login')

    
#=====================================================================
#=============================HOME PAGE===============================
#=====================================================================
   

@login_required(login_url='login')
def home_page(request):
    
    user        = request.user
    
    patient     = Patient.objects.filter(user=user).first()
    
    employee    = Employee.objects.filter(user=user).first()
    
    is_employee = user.groups.filter(name='employee').exists()
    
    is_patient  = user.groups.filter(name='patient').exists()
    
    context     = {
        'patient': patient,
        'employee': employee,
        'user': user,
        'is_employee': is_employee,
        'is_patient': is_patient,
    }
    return render(request, 'home.html', context)

@login_required
def update_user(request):
    if request.method == 'POST':
        
        user_form = Update(request.POST, instance=request.user)
        
        if 'old_password' in request.POST and request.POST['old_password']:
            
            password_form = PasswordChangeForm(request.user, request.POST)
            
            if password_form.is_valid():
                
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important, to keep the user logged in
                
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form     = Update(instance=request.user)
        
        password_form = PasswordChangeForm(request.user)

    return render(request, 'update_user.html', {
                'user_form': user_form,
                'password_form': password_form})
            

#=========================================================================================
#=============================OPERATIONS ONLY FOR EMPLOYEES===============================
#=========================================================================================
   

@login_required 
@allowed_user(allowed_roles=['employee'])
def capacity_page(request):
    employee = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        form = ChangeCapacity(request.POST, instance=employee.clinic)
        if form.is_valid():
            form.save()
            messages.success(request, 'you have changed the capacity')
            return redirect('home')
    else:
        form = ChangeCapacity(instance=employee.clinic)
    return render(request, 'changecapacity.html', {'form': form})

@login_required
@allowed_user(allowed_roles=['employee'])
def current_visits(request):
    user         = request.user

    employee     = Employee.objects.get(user=user)

    clinic       = employee.clinic

    appointments = Appointment.objects.filter(clinic=clinic)

    # get search parameters
    search_id     = request.GET.get('search_id', '')
    search_date   = request.GET.get('search_date', '')
    search_status = request.GET.get('search_status', '')

    if search_id:
        appointments = appointments.filter(appointment_id=search_id)
    if search_date:
        appointments = appointments.filter(appointmentDate=search_date)
    if search_status:
        appointments = appointments.filter(status=search_status)

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        appointment    = Appointment.objects.get(appointment_id=appointment_id)
        action         = request.POST.get('action')
        if action == 'cancel':
            no_patient          = Patient.objects.get(name="No Patient")
            appointment.patient = no_patient
            appointment.status  = 'available'
            clinic              = appointment.clinic
            clinic.capacity    += 1
            appointment.save()
            return redirect('current_visits')
        elif action == 'finish':
            appointment.status = 'finished'
            appointment.save()
            return redirect('current_visits') 
        
    return render(request, 'current_visits.html',{'appointments':appointments})


    
#=======================================================================================
#=============================OPERATION ONLY FOR PATIENTS===============================
#=======================================================================================
   
@login_required
@allowed_user(allowed_roles=['patient'])
def appointment_register(request):
    if request.method == 'POST':
        appointment_id      = request.POST.get('new_appointment')
        
        appointment         = Appointment.objects.get(appointment_id=appointment_id)
        
        patient             = get_object_or_404(Patient, user=request.user)
        
        appointment.patient = patient
        
        appointment.status  = 'occupied'
        
        appointment.save()
        return redirect('visit_register')
    search_query = request.GET.get('search', '')
    if search_query:
        available_appointments = Appointment.objects.filter(Q(clinic__name__icontains=search_query) | Q(appointmentDate__icontains=search_query),
                                                            status='available')
    else:
        available_appointments = Appointment.objects.filter(status='available')
    context = {
        'available_appointments': available_appointments,
    }
    return render(request, 'appointment_form.html', context)



@login_required
@allowed_user(allowed_roles=['patient'])
def appointment_view(request):
    patient = get_object_or_404(Patient, user=request.user)
    if request.method == 'POST':
        if 'cancel' in request.POST:
            appointment_id = request.POST.get('cancel')
            
            appointment    = get_object_or_404(Appointment, appointment_id=appointment_id)
            
            if appointment.patient == patient:
                
                no_patient                   = Patient.objects.get(name="No Patient")
                
                appointment.patient          = no_patient
                
                appointment.status           = 'available'
                
                appointment.clinic.capacity += 1
                
                appointment.clinic.save()
                appointment.save()
                messages.success(request, 'Appointment cancelled successfully.')
                return redirect('home')
            else:
                messages.error(request, 'You can only cancel your own appointments.')
        elif 'reschedule' in request.POST:
            
            old_appointment_id = request.POST.get('reschedule')
            
            old_appointment    = get_object_or_404(Appointment, appointment_id=old_appointment_id)
            
            return redirect('reschedule', old_appointment_id=old_appointment.appointment_id)
        
    appointments = Appointment.objects.filter(patient=patient,status='occupied')
    return render(request, 'appointment_view.html', {'appointments': appointments,})

@login_required
@allowed_user(allowed_roles=['patient'])
def reschedule_appointment(request, old_appointment_id):
    
    patient         = get_object_or_404(Patient, user=request.user)
    
    old_appointment = get_object_or_404(Appointment, appointment_id=old_appointment_id)

    if request.method == 'POST':
        
        new_appointment_id = request.POST.get('new_appointment')
        
        new_appointment    = get_object_or_404(Appointment, appointment_id=new_appointment_id)

        if old_appointment.patient == patient and new_appointment.status == 'available':
            #<<<<<<<<< CHANGING OLD APPOINTMENT >>>>>>>>>>>
            no_patient                       = Patient.objects.get(name="No Patient")
            
            old_appointment.patient          = no_patient            
            
            old_appointment.status           = 'available'
            
            old_appointment.clinic.capacity += 1
            
            old_appointment.clinic.save()
            old_appointment.save()

            #<<<<<<<<< CHANGING NEW APPOINTMENT >>>>>>>>>>>
            new_appointment.patient          = patient
            
            new_appointment.status           = 'occupied'
            
            new_appointment.clinic.capacity -= 1
            
            new_appointment.clinic.save()
            new_appointment.save()

            messages.success(request, 'Appointment rescheduled successfully.')
            return redirect('home')
        else:
            messages.error(request, 'You can only reschedule your own appointments.')
    else:
        search_query = request.GET.get('search', '')
        if search_query:
            appointments = Appointment.objects.filter(Q(clinic__name__icontains=search_query) | Q(appointmentDate__icontains=search_query), status='available')
        else:
            appointments = Appointment.objects.filter(status='available')
        return render(request, 'reschedule_appointment.html', {'available_appointments': appointments, 'old_appointment_id': old_appointment_id})
    

@login_required
@allowed_user(allowed_roles=['patient'])
def create_appointment(request):
    patient = get_object_or_404(Patient, user=request.user)
    if request.method == 'POST':
        appointment = AppointmentForm(request.POST)
        
        clinic_id   = request.POST.get('clinic') 
            
        clinic      = Clinic.objects.get(id=clinic_id)
        
        if clinic.availability:
            if appointment.is_valid():
                
                visit         = appointment.save(commit=False)
                
                visit.patient = patient  # set patient to the current user's patient
                
                visit.status  = 'occupied'
                
                
                visit.clinic = clinic
                visit.save()

                # Decrease the clinic's capacity by one
                clinic.capacity -= 1
                clinic.save()

                messages.success(request, 'Appointment booked successfully.')
                return redirect('home')      
        else:
                messages.error(request, 'The selected clinic is not available.')
                return redirect('home')
    appointment = AppointmentForm()
    return render(request, 'create_appointment.html',{'appointment': appointment})

@login_required
@allowed_user(allowed_roles=['patient'])
def appointment_history(request):
    
    patient               = get_object_or_404(Patient, user=request.user)
    
    finished_appointments = Appointment.objects.filter(patient=patient, status='finished')
    
    return render(request, 'appointment_history.html', {'finished_appointments': finished_appointments})