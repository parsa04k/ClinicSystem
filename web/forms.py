from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *


class Register(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
class PatientRegister(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name']
        
class EmployeeRegister(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['clinicID']