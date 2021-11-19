import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4b7738d07e309201c32d91d31cdd532d'

    error_msg = ""
    message = ""
    message_class = ""

    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data["name"]
            existing_city = City.objects.filter(name=new_city).count()
            if existing_city == 0:
                res = requests.get(url.format(new_city)).json()
                if res["cod"] == 200:
                    form.save()
                else:
                    error_msg = "City does not exist in the world"
            else:
                error_msg = "This city already exists in page"
        if error_msg:
            message = error_msg
            message_class = "is-danger"
        else:
            message = "City added successfully"
            message_class = "is-success"

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        res = requests.get(url.format(city)).json()

        city_weather = {
            "city": city.name,
            "temperature": res["main"]["temp"],
            "description": res["weather"][0]["description"],
            "icon": res["weather"][0]["icon"],
            "feel": res["main"]["feels_like"],
        }
        weather_data.append(city_weather)

    context = {
        "weather_data": weather_data,
        "form": form,
        "message": message,
        "message_class": message_class,
    }

    return render(request, "weather.html", context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect("home")

