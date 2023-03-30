from django.urls import path
from .views import home, day, singular_device_info,aboutus

urlpatterns = [
    
    path('',home, name="home"),
    path('daily',day, name = 'daily'),
    path('device/<str:name>', singular_device_info, name = "single"),
    path('about-us',aboutus,name = 'aboutus')
]