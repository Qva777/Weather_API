from django.urls import path
from weather_api import views

urlpatterns = [

    path('weather/current/', views.WeatherCurrentView.as_view(), name='current_weather'),
    path('weather/current_forecast/', views.WeatherCurrentForecastView.as_view(), name='current_weather_forecast'),

    path('weather/search/', views.WeatherSearchView.as_view(), name='search_weather'),
    path('weather/forecast/', views.WeatherForecastView.as_view(), name='weather_forecast'),
]
