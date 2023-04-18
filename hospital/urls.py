from django.urls import path, include
from hospitalapp.views import hospital_create, hospital_list, driver_page, update_hospital, home, navigate_to_destination, add_location, location_list


urlpatterns = [
    path('hospital/create/', hospital_create, name='hospital_create'),
    path('fd', hospital_list, name='hospital_list'),

    path('driver/', driver_page, name='driver_page'),
    path('hospital/<int:pk>/update/', update_hospital, name='update_hospital'),
    path('home/', home, name='home'),
    path('navigate/', navigate_to_destination, name='navigate_to_destination'),
    path('add_location/', add_location, name='add_location'),
    path('location_list/', location_list, name='location_list'),
    path('', include('api.urls')),
]
