from django.shortcuts import render, redirect, get_object_or_404
import requests
from .forms import HospitalForm
from .forms import LocationForm
from .models import Hospital
from .models import Location
import json
import hospital.settings as settings
from .models import Location, Hospital
import time
from datetime import datetime
import psutil



def hospital_create(request):
    """
    hospital_create view function renders the hospital_form.html template # Docstring
    """
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hospital_list')
    else:
        form = HospitalForm()
    return render(request, 'hospital/hospital_form.html', {'form': form})


def hospital_list(request):
    """
    hospital_list view function renders the hospital_list.html template # Docstring
    """
    hospitals = Hospital.objects.all()
    return render(request, 'hospital/hospital_list.html', {'hospitals': hospitals})


def hospital_update(request, hospital_id):
    hospital = Hospital.objects.get(id=hospital_id)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('hospital_list')
    else:
        form = HospitalForm(instance=hospital)
    return render(request, 'hospital/hospital_form.html', {'form': form})


def driver_page(request):
    """
    driver_page view function renders the driver_page.html template # Docstring 
    """
    hospitals = Hospital.objects.all()
    context = {'hospitals': hospitals}
    return render(request, 'hospital/driver_page.html', context)


def update_hospital(request, pk):
    """
    update_hospital view function renders the update_hospital.html template # Docstring
    """
    # hospital = Hospital.objects.get(id=hospital_id)
    hospital = get_object_or_404(Hospital, pk=pk)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('driver_page')
    else:
        form = HospitalForm(instance=hospital)
    context = {'form': form}
    return render(request, 'hospital/update_hospital.html', context)


def delete_hospital(request, pk):
    """
    delete_hospital view function renders the delete_hospital.html template # Docstring
    """
    hospital = get_object_or_404(Hospital, pk=pk)
    hospital.delete()
    return redirect('driver_page')


def home(request):
    return render(request, 'home.html')

def monitor_performance(func):
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        start_time = time.perf_counter()
        memory_before = process.memory_info().rss
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        memory_after = process.memory_info().rss
        execution_time = end_time - start_time
        memory_diff = memory_after - memory_before
        with open('performance_log.txt', 'a') as file:
            file.write(f'{func.__name__} executed in {execution_time:.6f} seconds and used {memory_diff / 1024 / 1024:.2f} MB of memory\n')
        return result
    return wrapper


@monitor_performance
def navigate_to_destination(request):
    """
    navigate_to_destination view function renders the navigate_to_destination.html template # Docstring
    """
    url = 'https://www.googleapis.com/geolocation/v1/geolocate'
    params = {'key': settings.GOOGLE_MAP}

    # Send a POST request to the Geolocation API endpoint
    response = requests.post(url, params=params)

    # Parse the JSON response and extract the latitude and longitude coordinates
    result = json.loads(response.text)
    lat = result['location']['lat']
    lng = result['location']['lng']

    # Step 2: Use the Google Maps Directions API to generate turn-by-turn directions

    # Set up the Directions API endpoint and parameters
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'origin': f'{lat},{lng}',
        'destination': 'Bangalore, India',
        'mode': 'driving',
        'key': settings.GOOGLE_MAP
    }

    # Send a GET request to the Directions API endpoint
    response = requests.get(url, params=params)

    # Parse the JSON response and extract the turn-by-turn directions
    result = json.loads(response.text)
    steps = result['routes'][0]['legs'][0]['steps']

    # Step 3: Use a navigation app on the user's mobile device to display the directions

    # Construct the navigation app URL and redirect the user to it
    url = f'https://www.google.com/maps/dir/?api=1&origin={lat},{lng}&destination=Bangalore, India&travelmode=driving'
    return redirect(url)

def navigates(request):
    # Step 1: Use the Google Maps Geocoding API to convert the destination address to geographic coordinates
    
    # Set up the Geocoding API endpoint and parameters
    address = 'karur'
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': address,
        'key': 'AIzaSyA5dTEWkBN0LKVc6APv6s1qSD0FyZzUTeM'
    }
    
    # Send a GET request to the Geocoding API endpoint
    response = requests.get(url, params=params)
    
    # Parse the JSON response and extract the destination latitude and longitude coordinates
    result = json.loads(response.text)
    lat2 = result['results'][0]['geometry']['location']['lat']
    lng2 = result['results'][0]['geometry']['location']['lng']
    lat1 = 13.05557
    lng1 = 80.1801294
    # Step 2: Use the A* algorithm to find the shortest path from the user's current location to the destination
    
    # Define a function to calculate the distance between two points
    def distance(lat1, lng1, lat2, lng2):
        return ((lat2 - lat1) ** 2 + (lng2 - lng1) ** 2) ** 0.5
    
    # Define a function to generate the neighbors of a node on the map
    def neighbors(lat, lng):
        # Set up the Google Maps Places API endpoint and parameters
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        params = {
            'location': f'{lat},{lng}',
            'radius': 1000,
            'type': 'point_of_interest',
            'key': 'AIzaSyA5dTEWkBN0LKVc6APv6s1qSD0FyZzUTeM'
        }
        
        # Send a GET request to the Places API endpoint
        response = requests.get(url, params=params)
        
        # Parse the JSON response and extract the neighboring latitude and longitude coordinates
        results = json.loads(response.text)
        return [(result['geometry']['location']['lat'], result['geometry']['location']['lng']) for result in results['results']]
    
    # Define the A* algorithm
    def a_star(start, goal, neighbors_fn, distance_fn):
        # Initialize the frontier and explored sets
        frontier = [(start, 0, None)]
        explored = set()
        
        # Loop until the frontier is empty
        while frontier:
            # Choose the node with the lowest estimated cost to the goal
            current, cost, parent = min(frontier, key=lambda x: x[1] + distance_fn(x[0][0], x[0][1], goal[0], goal[1]))
            
            # If we've reached the goal, reconstruct the path and return it
            if current == goal:
                path = [current]
                while parent:
                    path.append(parent)
                    parent = parent[2]
                return list(reversed(path))
            
            # Otherwise, add the current node to the explored set and generate its neighbors
            explored.add(current)
            for neighbor in neighbors_fn(*current):
                if neighbor not in explored:
                    # Add the neighbor to the frontier with the estimated cost
                    new_cost = cost + distance_fn(*current, *neighbor)
                    frontier.append((neighbor, new_cost, current))
        
        # If we've explored the entire map without finding the goal, return None
        return None
    
    # Get the user's current location from the browser's geolocation API
    # (Note: This requires user permission and may not
    # be available on all devices or
     # Step 3: Use the Google Maps Directions API to generate turn-by-turn directions for the user
    
    # Generate the directions for the user
    directions_url = "https://www.google.com/maps/dir/?api=1&origin=" + str(lat1) + "," + str(lng1) + "&destination=" + str(lat2) + "," + str(lng2) + "&travelmode=driving"
    
    # Return the directions to the user
    return redirect(directions_url)
    try:
     # Get the starting and ending coordinates from the user input
         start_lat = float(request.GET.get('start_lat'))
         start_lng = float(request.GET.get('start_lng'))
         end_lat = float(request.GET.get('end_lat'))
         end_lng = float(request.GET.get('end_lng'))

        # Call the A* algorithm to get the shortest path
         path = astar(start_lat, start_lng, end_lat, end_lng)

        # Convert the path to a format that can be displayed on the map
         path_json = json.dumps(path)

        # Return the path as a JSON response
         return HttpResponse(path_json, content_type='application/json')
   
    except Exception as e:
        # Return an error message if any exception occurs
         return HttpResponse('Error: ' + str(e))

def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_list')
    else:
        form = LocationForm()
    return render(request, 'location/add_location.html', {'form': form})


def location_list(request):
    locations = Location.objects.all()
    return render(request, 'location/location_list.html', {'locations': locations})