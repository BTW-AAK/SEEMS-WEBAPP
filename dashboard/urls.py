from django.urls import path
from .views import home, day

urlpatterns = [
    
    path('',home, name="home"),
    path('daily',day, name = 'daily')
    
]