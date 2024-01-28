from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from .decoators import *
from .functions import *

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@unauthenticated_user
def patient_register_page(request):
    form      = Register()
    name_form = PatientRegister()
    if request.method=='POST' :
        form = Register(request.POST)
        name_form = PatientRegister(request.POST)
        if form.is_valid() and name_form.is_valid():
            user = form.save()
            patient = name_form.save(commit=False)
            group = Group.objects.get(name='patient')
            user.groups.add(group)
            patient.user = user
            patient.save()
            messages.success(request, f"Account created for {form.cleaned_data.get('username')}")
            return redirect('login')
            
    context = {'form' :form,'name_form':name_form}
    return render(request, 'register_patient.html', context)

@unauthenticated_user
def employee_register_page(request):
    form = Register()
    clinic_form = EmployeeRegister()
    if request.method=='POST' :
        form = Register(request.POST)
        clinic_form = EmployeeRegister(request.POST)
        if form.is_valid() and clinic_form.is_valid():
            user = form.save()
            employee = clinic_form.save(commit=False)
            group = Group.objects.get(name='employee')
            user.groups.add(group)
            employee.user = user
            employee.save()
            messages.success(request, f"Account created for {form.cleaned_data.get('username')}")
            return redirect('login')
            
    context = {'form' :form, 'clinic_form':clinic_form}
    return render(request, 'register_employee.html', context)

@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        login_id = request.POST.get('login_id')  # can be username or email
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

def forgot_password(request):
    """View to handle forgot password requests"""
    temp_password = None
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            temp_password = generate_temp_password()
            user.set_password(temp_password)
            user.save()
            #return redirect('login')
    # render forgot password form
    return render(request, 'forgot_password.html', {'temp_password': temp_password})

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home_page(request):
    user = request.user
    is_employee = user.groups.filter(name='employee').exists()
    is_patient = user.groups.filter(name='patient').exists()
    context = {
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
        user_form = Update(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'update_user.html', {
        'user_form': user_form,
        'password_form': password_form})