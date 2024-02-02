from django.db import models
from django.contrib.auth.models import User

class Clinic(models.Model):
    id           = models.IntegerField(primary_key=True)
    name         = models.TextField(max_length = 20)
    address      = models.TextField(max_length = 255)
    services     = models.TextField(max_length = 255)
    availability = models.BooleanField()
    capacity     = models.PositiveIntegerField()
    
    def save(self, *args, **kwargs):
        if self.capacity <= 0:
            self.capacity = 0
            self.availability = False
        else: 
            self.availability = True
        super().save(*args, **kwargs)

    

class Patient(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    name        = models.CharField(max_length = 20, null=True,blank=True)
    admitDate   = models.DateField(auto_now=True)
    status      = models.BooleanField(default=False)
    
class Employee(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    name        = models.CharField(max_length = 20, null=True,blank=True)
    admitDate   = models.DateField(auto_now=True)
    status      = models.BooleanField(default=False)
    clinic      = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True)
    
class Appointment(models.Model):
    STATUS_OF_APPOINTMENT = {
        ('occupied','Occupied'),
        ('available','Available'),
        ('finished','Finished')
    }
    appointment_id  = models.AutoField(primary_key=True, default=None)
    patient         = models.ForeignKey(Patient, on_delete=models.CASCADE, default=None)
    clinic          = models.ForeignKey(Clinic,  on_delete=models.CASCADE, default=None)
    appointmentDate = models.DateField()
    status          = models.TextField(default='available', choices=STATUS_OF_APPOINTMENT)
