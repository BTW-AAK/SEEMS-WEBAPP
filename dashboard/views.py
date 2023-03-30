from django.shortcuts import render
from .models import Consumption_Data, Device
from django.utils import timezone
from datetime import timedelta
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
	    'devices':devices,
    })

def singular_device_info(request,name):
    devices = Device.objects.all()
    device = Device.objects.get(device_name = name)

    now = timezone.now()
    
    energy_used = Consumption_Data.objects.order_by('-starttime').filter(device_id = device.device_id, starttime__gte=now-timedelta(days=7))
    e = [x.energy for x in energy_used]
    
    
    energy_consumed_on_day ={}
    for entry in energy_used:
        date = entry.starttime.strftime("%Y-%m-%d")
        
        if date in energy_consumed_on_day:
            energy_consumed_on_day[date] += entry.energy
        else:
            energy_consumed_on_day[date] = entry.energy
    try:
        mx = max(energy_consumed_on_day.items(), key = lambda x: x[1])[1]
    except ValueError:
        mx =0
    
    data = list(energy_consumed_on_day.items())
    print(data)
    context = {'name':name,
               'devices':devices,
               'mx':mx,
               'data':data,

    }
        
    return render(request,'dashboard/device.html',context)

def aboutus(request):
    return render(request, 'dashboard/aboutus.html')
