from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, Permission


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

database = {                                               
    "1": 25,                                               
    "2": 15,                                                
    "3": 15,                                                   
    "4": 20,                                                   
    "5": 30,
    "6": 9,
    "7": 8
}


# Register your models here.
Group.objects.get_or_create(name='patient')
Group.objects.get_or_create(name='employee]')


# Clinic with capacity 25
clinic2 = Clinic(id=2, name='Clinic 2', address='223 Main St', services='General Practice', availability=True, capacity=25)
clinic2.save()

# Clinic with capacity 15
clinic3 = Clinic(id=3, name='Clinic 3', address='323 Main St', services='General Practice', availability=True, capacity=15)
clinic3.save()

# Another clinic with capacity 15
clinic4 = Clinic(id=4, name='Clinic 4', address='423 Main St', services='General Practice', availability=True, capacity=15)
clinic4.save()

# Clinic with capacity 20
clinic5 = Clinic(id=5, name='Clinic 5', address='523 Main St', services='General Practice', availability=True, capacity=20)
clinic5.save()

# Clinic with capacity 30
clinic6 = Clinic(id=6, name='Clinic 6', address='623 Main St', services='General Practice', availability=True, capacity=30)
clinic6.save()

# Clinic with capacity 9
clinic7 = Clinic(id=7, name='Clinic 7', address='723 Main St', services='General Practice', availability=True, capacity=9)
clinic7.save()

# Clinic with capacity 8
clinic8 = Clinic(id=8, name='Clinic 8', address='823 Main St', services='General Practice', availability=True, capacity=8)
clinic8.save()

