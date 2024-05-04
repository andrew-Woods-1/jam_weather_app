from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from datetime import datetime


# Create your views here.

# index view to handle app logic
def index(request):
    # try block if POST
    try:
    # checking if the method is POST
        if request.method == 'POST':

            # Store the API key in a constant variable
            API_KEY = '7fbda08677dac82a98a9081c2ae362bc'

            # getting the city name from the form input   
            city_name = request.POST.get('city')

            # the url for current weather, takes city_name and API_KEY variables 
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=imperial'

            # get the response
            response = requests.get(url).json()

            # Use the response to get the entered city's latitude and longitude
            lat = response['coord']['lat']
            lon = response['coord']['lon']
            limit = 2

            # Access the GeoCoding API to get the value of the state the city exists in, if any
            url_state = f'http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit={limit}&appid={API_KEY}'

            # Create new response object for this API call
            response_state = requests.get(url_state).json()

            # get the current time
            current_time = datetime.now()
            # format the time
            formatted_time = current_time.strftime("%A, %B %d %Y, %H:%M:%S %p")

            # create the dictionary with values supplied from API
            city_weather_update = {
                'city': city_name + ",",
                'state': response_state[0]['state'],
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
                'temperature': 'Temperature: ' + str(response['main']['temp']) + ' °F',
                'real_feel': 'Feels Like: ' +str(response['main']['feels_like']) + ' °F',
                'daily_max' : 'Daily High: ' + str(response['main']['temp_max']) + ' °F',
                'daily_min' : 'Daily Low: ' + str(response['main']['temp_min']) + ' °F',
                'country_code': response['sys']['country'],
                'wind': 'Wind: ' + str(response['wind']['speed']) + ' mph',
                'humidity': 'Humidity: ' + str(response['main']['humidity']) + '%',
                'time': formatted_time
            }
        # if the request method is GET empty the dictionary
        else:
            city_weather_update = {}
        context = {'city_weather_update': city_weather_update}

        # render the page with the supplied data
        return render(request, 'weather_updates/home.html', context)
    
    # Catch errors and render the 404.html page
    except:
        return render(request, 'weather_updates/404.html')