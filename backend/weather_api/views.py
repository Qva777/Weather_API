import requests
from datetime import datetime, timedelta
from django.conf import settings

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class WeatherDataMixin:
    """ Mixin class for common weather data retrieval and processing methods """

    @staticmethod
    def get_weather_data(base_url, params):
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise requests.RequestException(f"Error retrieving weather data: {str(e)}")

    @staticmethod
    def extract_current_weather_info(data):
        """ Extract relevant information from current weather data """
        return {
            'time': datetime.now().strftime('%H:%M'),
            'country': data['sys']['country'],
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'datetime': datetime.now().strftime('%d %B %Y'),
        }

    @staticmethod
    def extract_location_info(data):
        """ Extract city and country information from weather data """
        return data['city']['name'], data['city']['country']

    @staticmethod
    def extract_forecast_info(data, city_name, country):
        """ Extract forecast information from weather data """
        forecast_info = []

        for entry in data['list']:
            formatted_date = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S')
            formatted_date_str = formatted_date.strftime('%d %B %Y')
            time = formatted_date.strftime('%H:%M')

            forecast_info.append({
                'time': time,
                'country': country,
                'city': city_name,
                'temperature': entry['main']['temp'],
                'description': entry['weather'][0]['description'],
                'datetime': formatted_date_str,
            })

        return forecast_info

    @staticmethod
    def filter_forecast_for_next_7_days(forecast_info):
        """ Filter forecast information for the next 7 days """
        return [entry for entry in forecast_info if
                datetime.strptime(entry['datetime'], '%d %B %Y') <= datetime.now() + timedelta(days=7)]


class WeatherCurrentView(APIView, WeatherDataMixin):
    """ GET the current weather based on the user's IP address """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_ip = self.get_client_ip(request)

        ipinfo_url = f'https://ipinfo.io/{user_ip}/json'
        ipinfo_response = requests.get(ipinfo_url)
        ipinfo_data = ipinfo_response.json()

        loc = ipinfo_data.get('loc', '')
        if not loc or ',' not in loc:
            return Response({"detail": "Unable to determine user location."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        latitude, longitude = loc.split(',')
        api_key = settings.OPENWEATHERMAP_API_KEY

        base_url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'lat': latitude,
            'lon': longitude,
            'appid': api_key,
            'units': 'metric',
        }

        data = self.get_weather_data(base_url, params)

        weather_info = self.extract_current_weather_info(data)

        return Response({"current_weather_data": weather_info}, status=status.HTTP_200_OK)

    @staticmethod
    def get_client_ip(request):
        """ Get the client's IP address from the request """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class WeatherSearchView(APIView, WeatherDataMixin):
    """ GET the current weather based on the provided city name or zip code """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            query = request.query_params.get('query', None) or request.data.get('query', None)

            if not query:
                return Response({"detail": "Please provide a city name or zip code"},
                                status=status.HTTP_400_BAD_REQUEST)

            base_url = 'https://api.openweathermap.org/data/2.5/weather'
            params = {
                'q': query,
                'zip': query,
                'appid': settings.OPENWEATHERMAP_API_KEY,
                'units': 'metric',
            }

            data = self.get_weather_data(base_url, params)

            weather_info = self.extract_current_weather_info(data)

            return Response({"current_weather_data": weather_info}, status=status.HTTP_200_OK)

        except Exception as e:
            error_message = f"Check that the entered data is correct:  {str(e)}"
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WeatherForecastView(APIView, WeatherDataMixin):
    """ GET the weather forecast for the next 7 days based on the provided city name or zip code """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            query = request.query_params.get('query', None) or request.data.get('query', None)

            if not query:
                return Response({"detail": "Please provide a city name or zip code"},
                                status=status.HTTP_400_BAD_REQUEST)

            base_url = 'https://api.openweathermap.org/data/2.5/forecast'
            api_key = settings.OPENWEATHERMAP_API_KEY

            params = {
                'q': query,
                'zip': query,
                'appid': api_key,
                'units': 'metric',
            }

            data = self.get_weather_data(base_url, params)

            city_name, country = self.extract_location_info(data)

            forecast_info = self.extract_forecast_info(data, city_name, country)

            next_7_days_forecast = self.filter_forecast_for_next_7_days(forecast_info)

            return Response({"next_7_days_forecast": next_7_days_forecast}, status=status.HTTP_200_OK)

        except Exception as e:
            error_message = f"Check that the entered data is correct:  {str(e)}"
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WeatherCurrentForecastView(WeatherCurrentView):
    """ GET the current weather and forecast for the next 7 days based on the user's IP address """

    def get(self, request):
        current_weather_response = super().get(request)

        if current_weather_response.status_code != status.HTTP_200_OK:
            return current_weather_response

        current_weather_data = current_weather_response.data.get("current_weather_data", {})

        city_name = current_weather_data.get("city", "")

        forecast_response = self.get_7_days_forecast(city_name, current_weather_data)

        return forecast_response

    def get_7_days_forecast(self, city_name, current_weather_data):
        """ Add logic to get the weather forecast for the next 7 days """
        try:
            base_url = 'https://api.openweathermap.org/data/2.5/forecast'
            api_key = settings.OPENWEATHERMAP_API_KEY

            params = {
                'q': city_name,
                'appid': api_key,
                'units': 'metric',
            }

            data = self.get_weather_data(base_url, params)

            city_name, country = self.extract_location_info(data)
            forecast_info = self.extract_forecast_info(data, city_name, country)
            next_7_days_forecast = self.filter_forecast_for_next_7_days(forecast_info)

            response_data = {
                "current_weather_data": current_weather_data,
                "next_7_days_forecast": next_7_days_forecast
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            error_message = f"Error retrieving forecast data: {str(e)}"
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
