from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=a1ab38bfb95b2234257bac9029a7e53b'

    cities = City.objects.all()
    weather_data = []

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        if form.is_valid(): # will validate and save if valid
            form.save()

    form = CityForm()

    for city in cities:
        response = requests.get(url.format(city.name))
        if response.status_code == 200:
            city_weather = response.json()
            if 'main' in city_weather and 'weather' in city_weather:
                weather = {
                    'city' : city.name,
                    'temperature' : city_weather['main']['temp'],
                    'description' : city_weather['weather'][0]['description'],
                    'icon' : city_weather['weather'][0]['icon']
                }
            else:
                weather = {
                    'city' : city.name,
                    'temperature' : 'N/A',
                    'description' : 'N/A',
                    'icon' : ''
                }
        else:
            weather = {
                'city' : city.name,
                'temperature' : 'N/A',
                'description' : 'N/A',
                'icon' : ''
            }
        
        weather_data.append(weather)

    context = {
        'weather_data' : weather_data,
        'form' : form
    }

    return render(request, 'weather/index.html', context) #returns the index.html template with the context
