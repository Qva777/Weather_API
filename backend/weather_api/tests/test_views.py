from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from unittest.mock import patch

User = get_user_model()


class WeatherViewsTestCase(TestCase):
    def setUp(self):
        """ Set up test environment """
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.weather_search_url = '/api/weather/search/'
        self.weather_forecast_url = '/api/weather/forecast/'

    def authenticate_user(self):
        """ Authenticate the test user """
        self.client.force_authenticate(user=self.user)

    @patch('requests.get')
    def test_search_weather_view(self, mock_get):
        """ Test the search weather view """
        self.authenticate_user()

        # Mocking the response from the weather API
        mock_response = {
            'sys': {'country': 'US'},
            'name': 'New York',
            'main': {'temp': 14.21},
            'weather': [{'description': 'clear sky'}]
        }
        mock_get.return_value.json.return_value = mock_response

        response = self.client.get(self.weather_search_url, {'query': 'New York'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('current_weather_data', data)
        self.assertIn('time', data['current_weather_data'])
        self.assertIn('country', data['current_weather_data'])
        self.assertIn('city', data['current_weather_data'])
        self.assertIn('temperature', data['current_weather_data'])
        self.assertIn('description', data['current_weather_data'])
        self.assertIn('datetime', data['current_weather_data'])

    @patch('requests.get')
    def test_forecast_weather_view(self, mock_get):
        """ Test the forecast weather view """
        self.authenticate_user()

        # Mocking the response from the weather API
        mock_response = {
            'city': {'name': 'New York', 'country': 'US'},
            'list': [
                {
                    'dt_txt': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S'),
                    'main': {'temp': 20},
                    'weather': [{'description': 'clear sky'}]
                } for i in range(7)
            ]
        }
        mock_get.return_value.json.return_value = mock_response

        response = self.client.get(self.weather_forecast_url, {'query': 'New York'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('next_7_days_forecast', data)
        self.assertTrue(isinstance(data['next_7_days_forecast'], list))
        self.assertEqual(len(data['next_7_days_forecast']), 7)


