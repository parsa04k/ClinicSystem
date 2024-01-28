from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, Permission

# Register your models here.
Group.objects.get_or_create(name='patient')
Group.objects.get_or_create(name='employee]')

class ClinicAdmin(admin.ModelAdmin):
    pass
admin.site.register(Clinic, ClinicAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Employee, EmployeeAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)
