from django.shortcuts import render
from .models import Consumption_Data
import datetime
# Create your views here.
def home(request):
    now = datetime.datetime.now()
    objs =Consumption_Data.objects.filter(starttime__month=now.month)
    total_power = 0
    for o in objs :
        total_power+=o.energy

    print(total_power)
    context = {'power':total_power}
    return render(request, 'dashboard/index.html',context)

