from django.contrib import admin
from .models import Consumption, Device,Consumption_Data
# Register your models here.

admin.site.register(Consumption)
admin.site.register(Device)
admin.site.register(Consumption_Data)