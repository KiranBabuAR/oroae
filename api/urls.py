from . import views
from django.urls import path

urlpatterns = [
    path('fd/', views.getLocation, name='getLocation'),
    path('df/', views.getHospital, name='getHospital')
]