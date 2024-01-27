from django.db import models
from django.contrib.auth.models import User

class Clinic(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    address = models.TextField()
    services = models.TextField()
    availability = models.BooleanField()
    capacity = models.PositiveIntegerField()
    

class Patient(models.Model):
    user        = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length = 20, null=True,blank=True)
    admitDate   = models.DateField(auto_now=True)
    status      = models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    
class Employee(models.Model):
    user        = models.OneToOneField(User,on_delete=models.CASCADE)
    admitDate   = models.DateField(auto_now=True)
    status      = models.BooleanField(default=False)
    clinicID    = models.PositiveIntegerField()
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    
class Appointment(models.Model):
    STATUS_OF_APPOINTMENT = {
        ('occupied','Occupied'),
        ('available','Available'),
        ('finished','Finished')
    }
    patientId=models.PositiveIntegerField(null=True)
    clinicID=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    status=models.TextField(default='available', choices=STATUS_OF_APPOINTMENT)
