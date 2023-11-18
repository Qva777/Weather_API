from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from clients.models import CustomUser


class CreateUserAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """ Test creating a new user """
        url = reverse('create_user')
        data = {'username': 'testuser', 'password': 'testpassword'}

        response = self.client.post(url, data, format='json')

        # Check that the response is successful and user is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'testuser')


class UserAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username='existinguser', password='existingpassword')
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.client.logout()

    def test_get_user_list(self):
        """ Test retrieving the list of users """
        url = reverse('user_list')
        response = self.client.get(url)

        # Check that the response is successful and contains the expected data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_user_detail(self):
        """ Test retrieving details of a specific user """
        url = reverse('user_detail', args=[self.user.id])
        response = self.client.get(url)

        # Check that the response is successful and contains the expected user details
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existinguser')

    def test_update_user(self):
        """ Test updating user details """
        url = reverse('user_detail', args=[self.user.id])
        data = {'username': 'updateduser', 'password': 'updatedpassword'}

        response = self.client.put(url, data, format='json')

        # Check that the response is successful and user details are updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.get(id=self.user.id).username, 'updateduser')

    def test_delete_user(self):
        """ Test deleting a user """
        url = reverse('user_detail', args=[self.user.id])

        response = self.client.delete(url)

        # Check that the response is successful and the user is deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 0)
