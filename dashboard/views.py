from django.shortcuts import render
from .models import Consumption
import datetime
# Create your views here.
def home(request):
    now =datetime.datetime.now()
    objs =Consumption.objects.filter(current_date__month='03')
    total_power = 0
    for o in objs :
        total_power+=o.power

    print(total_power)
    context = {'power':total_power}
    return render(request, 'dashboard/index.html',context)

