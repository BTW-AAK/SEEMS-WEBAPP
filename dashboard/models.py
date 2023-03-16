from django.db import models
from django.utils import timezone

class Consumption(models.Model):
    power= models.IntegerField()
    current_date = models.DateTimeField(default = timezone.now)
    device_name= models.CharField(max_length=50)
    

    def __str__(self):
        return f"{self.device_name}"
    
class Device(models.Model):
    device_name = models.CharField(max_length=50)
    device_ip = models.CharField(max_length=50)
    device_id = models.CharField(max_length=50)
    device_key = models.CharField(max_length=50)
    device_version = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.device_name}"
    

# device , energy consumed, starttime, end time, 
class Consumption_Data(models.Model):
    device_id = models.CharField(max_length=50)
    energy = models.FloatField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()

    def __str__(self):
        return f"{self.device.device_name} |{self.energy}KWh"
