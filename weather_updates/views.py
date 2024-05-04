from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from datetime import datetime


# Create your views here.

# the index() will handle all the app's logic
def index(request):
    # if there are no errors the code inside try will execute
    try:
    # checking if the method is POST
        if request.method == 'POST':
            API_KEY = '7fbda08677dac82a98a9081c2ae362bc'
            # getting the city name from the form input   
            city_name = request.POST.get('city')

            # the url for current weather, takes city_name and API_KEY   
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=imperial'
            # converting the request response to json   
            response = requests.get(url).json()

            lat = response['coord']['lat']
            lon = response['coord']['lon']
            limit = 2

            url_state = f'http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit={limit}&appid={API_KEY}'
            response_state = requests.get(url_state).json()


            # getting the current time
            current_time = datetime.now()
            # formatting the time using directives, it will take this format Day, Month Date Year, Current Time 
            formatted_time = current_time.strftime("%A, %B %d %Y, %H:%M:%S %p")
            # bundling the weather information in one dictionary
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
        return render(request, 'weather_updates/home.html', context)
    # if there is an error the 404 page will be rendered 
    # the except will catch all the errors 
    except:
        return render(request, 'weather_updates/404.html')