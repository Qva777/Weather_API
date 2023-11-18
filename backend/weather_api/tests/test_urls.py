from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status


class WeatherAPITests(APITestCase):
    """ Weather API Tests """

    def setUp(self):
        """ Create a test user """
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def authenticate_user(self):
        """ Authenticate the test user """
        self.client.force_authenticate(user=self.user)

    def test_search_weather_view(self):
        """ Ensure that the view returns a 200 response for authenticated users """
        self.authenticate_user()
        response = self.client.get('/api/weather/search/?query=London')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forecast_view(self):
        """ Ensure that the view returns a 200 response for authenticated users """
        self.authenticate_user()
        response = self.client.get('/api/weather/forecast/?query=Paris')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_access(self):
        """ Ensure that unauthenticated users are denied access """
        response = self.client.get('/api/weather/current/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_query_params(self):
        """ Ensure that views handle invalid or missing query parameters properly """
        self.authenticate_user()

        # Test invalid query parameter for search
        response_search = self.client.get('/api/weather/search/')
        self.assertEqual(response_search.status_code, status.HTTP_400_BAD_REQUEST)

        # Test invalid query parameter for forecast
        response_forecast = self.client.get('/api/weather/forecast/')
        self.assertEqual(response_forecast.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unable_to_determine_location(self):
        """
        Ensure that the current weather view handles cases where user location cannot be determined
        """
        self.authenticate_user()
        response = self.client.get('/api/weather/current/')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('Unable to determine user location', response.data['detail'])
