from django.shortcuts import render
from django.contrib import messages
from django.views.generic import View
from .forms import SearchForm
import requests
from datetime import datetime


def icons(icon):
    d={
        '01d': 'https://cdn-icons-png.flaticon.com/128/4814/4814268.png',
        '01n': 'https://cdn-icons-png.flaticon.com/128/9689/9689786.png',
        '02d': 'https://cdn-icons-png.flaticon.com/128/1163/1163661.png',
        '02n': 'https://cdn-icons-png.flaticon.com/128/5903/5903541.png',
        '03d': 'https://cdn-icons-png.flaticon.com/128/3208/3208676.png',
        '03n': 'https://cdn-icons-png.flaticon.com/128/2929/2929984.png',
        '04d': 'https://cdn-icons-png.flaticon.com/128/3208/3208676.png',
        '04n': 'https://cdn-icons-png.flaticon.com/128/2929/2929984.png',
        '09d': 'https://cdn-icons-png.flaticon.com/128/12276/12276729.png',
        '09n': 'https://cdn-icons-png.flaticon.com/128/5812/5812782.png',
        '11d': 'https://cdn-icons-png.flaticon.com/128/4724/4724103.png',
        '11n': 'https://cdn-icons-png.flaticon.com/128/1959/1959334.png',
        '13d': 'https://cdn-icons-png.flaticon.com/128/642/642000.png',
        '13n': 'https://cdn-icons-png.flaticon.com/128/100/100825.png',
        '50d':'https://cdn-icons-png.flaticon.com/128/2675/2675962.png',
        '50n':'https://cdn-icons-png.flaticon.com/128/106/106052.png'
    }

    return d[icon]
    
    

def fetch_data(city):
    API_key =  'c2b682ea804cb86416eaf1c244f4ec6c'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"

    data = requests.get(url).json()

    
    temperature = data['main']['temp'] - 273.15
    min_temperature = data['main']['temp_min'] - 273.15
    max_temperature = data['main']['temp_max'] - 273.15
    description = data['weather'][0]['main']
    icon = data['weather'][0]['icon']
    visibility_km = data['visibility'] / 1000  # Convert meters to kilometers
    wind_speed_kmh = data['wind']['speed'] * 3.6  # Convert m/s to km/h
    humidity = data['main']['humidity']

    # Determine if it's day or night based on sunset and sunrise times
    sunset_time = data['sys']['sunset']
    sunrise_time = data['sys']['sunrise']


    time_stamp = data['dt']
    date_object = datetime.utcfromtimestamp(time_stamp)
    date = date_object.strftime('%A, %d %B %Y')

    is_day = sunrise_time < time_stamp < sunset_time

    country= data['sys']['country']

    icon_url = icons(icon)

    weather={'city':city,
             'temp':round(temperature),
             'min_temp':round(min_temperature),
             'max_temp':round(max_temperature),
             'desc':str.capitalize(description),
             'visibility':round(visibility_km),
             'is_day':is_day,
             'wind_speed':round(wind_speed_kmh),
             'current_time':str(date).split(),
             'humidity':humidity,     
             'country':country,
             'icon':icon_url,        
             }

    print(weather)
    return weather


class Home(View):
    template_name = 'app\home.html'

    def get(self, request):
        form = SearchForm()
        return render(request, self.template_name, {'form': form} )

    def post(self, request):
        form = SearchForm(request.POST)

        if form.is_valid():
            city = form.cleaned_data['search']
            data = None
            exception_occured = False

            try:
                data = fetch_data(city)

            except KeyError:
                exception_occured = True
                messages.error(request,'Entered data is not available to API') 

            return render(request, self.template_name, {'form': form, "data":data, 'exception_occured':exception_occured})

        return render(request, self.template_name, {'form': form} )
