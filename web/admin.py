from django.contrib import admin
from .models import *
# Register your models here.
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
