from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *


class Register(UserCreationForm):
    class Meta:
        model  = User
        fields = ['username','email','password1','password2']
        
class PatientRegister(forms.ModelForm):
    class Meta:
        model  = Patient
        fields = ['name']
        
class EmployeeRegister(forms.ModelForm):
    clinic = forms.ModelChoiceField(
        queryset      = Clinic.objects.all(), 
        empty_label   = "(Nothing selected)",
        to_field_name = "id",
    )
    clinic.label_from_instance = lambda obj: f"{obj.name} (ID: {obj.id})"

    class Meta:
        model  = Employee
        fields = ['clinic','name']

    def save(self, commit=True):
        employee        = super(EmployeeRegister, self).save(commit=False)
        employee.clinic = self.cleaned_data['clinic']

        if commit:
            employee.save()

        return employee
    
        
class Update(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['first_name','email']
        
class ChangeCapacity(forms.ModelForm):
    class Meta:
        model  = Clinic
        fields = ['capacity']
        
class CancelAppointmentForm(forms.ModelForm):
    class Meta:
        model  = Appointment
        fields = ['appointment_id']

    def save(self, commit=True):
        appointment = super().save(commit=False)
        appointment.patient = None
        appointment.status  = 'available'

        if commit:
            appointment.save()

        return appointment

class AppointmentForm(forms.ModelForm):
    appointmentDate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    clinic = forms.ModelChoiceField(
        queryset      = Clinic.objects.all(), 
        empty_label   = "(Nothing selected)",
        to_field_name = "id",
    )
    clinic.label_from_instance = lambda obj: f"{obj.name} (ID: {obj.id})"
    class Meta:
        model  = Appointment
        fields = ['clinic', 'appointmentDate']