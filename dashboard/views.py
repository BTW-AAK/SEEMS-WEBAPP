from django.shortcuts import render
from .models import Consumption_Data, Device
from django.utils import timezone
# Create your views here.
def home(request):
    labels = []
    data =[]
    total = 0
    now = timezone.localtime(timezone.now())
    devices = Device.objects.all()

    for device in devices:
        queryset = Consumption_Data.objects.all()
        energy_consumed = 0
        for query in queryset:
            if query.device_id == device.device_id and query.starttime.month==now.month:
                
                energy_consumed +=query.energy
        name = device.device_name
        labels.append(name)
        data.append(energy_consumed)
    total = round(sum(data),4)
    return render(request, 'dashboard/index.html',{
        'labels': labels,
        'data' : data,
        'total':total,
	'devices':devices
    })

def day(request):

    labels = []
    data =[]
    total = 0
    if request.method =='POST':
        date = request.POST['date']
        if date:
            now = int(date.split('-')[2])
        else:
            now = timezone.localtime(timezone.now())
            now = now.day            
        
    else:
        
        now = timezone.localtime(timezone.now())
        now = now.day
    print(now)
    devices = Device.objects.all()

    for device in devices:

        queryset = Consumption_Data.objects.all()
        
        energy_consumed = 0
        for query in queryset:
            
            if query.device_id == device.device_id and query.starttime.day==now:
                
                energy_consumed +=query.energy
        name = device.device_name

        labels.append(name)
        data.append(energy_consumed)
        total = round(sum(data),4)
    
    return render(request, 'dashboard/day.html',{
        'labels': labels,
        'data' : data,
        'total':total,
	'devices':devices
    })

def singular_device_info(request,name):
	devices = Device.objects.all()
        
    
	return render(request,'dashboard/device.html', {'name':name})
