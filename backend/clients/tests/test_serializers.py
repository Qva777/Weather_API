from django.test import TestCase
from django.contrib.auth import get_user_model
from clients.serializers import CustomUserSerializer


class CustomUserSerializerTest(TestCase):
    def setUp(self):
        """ Create a test user for serialization """
        self.user_data = {'username': 'testuser', 'password': 'testpassword'}
        self.user = get_user_model().objects.create_user(**self.user_data)

        """ Create a serializer instance """
        self.serializer = CustomUserSerializer(instance=self.user)

    def test_serializer_contains_expected_fields(self):
        """ Ensure that the serializer contains the expected fields """
        expected_fields = ['id', 'username', 'password']
        actual_fields = list(self.serializer.fields.keys())
        self.assertEqual(expected_fields, actual_fields)

    def test_serializer_data_contains_expected_values(self):
        """ Ensure that the serialized data contains the expected values """
        expected_data = {'id': self.user.id, 'username': 'testuser'}

        serialized_data = self.serializer.data.copy()
        serialized_data.pop('password', None)

        self.assertEqual(serialized_data, expected_data)

    def test_serializer_create_method(self):
        """ Test the create method of the serializer """
        user_data = {'username': 'newuser', 'password': 'newpassword'}
        serializer = CustomUserSerializer(data=user_data)

        # Ensure serializer is valid
        self.assertTrue(serializer.is_valid())

        # Call create to create a new user
        new_user = serializer.create(user_data)

        # Ensure a new user is created with the provided data
        self.assertEqual(new_user.username, 'newuser')

    def test_serializer_update_method(self):
        """ Test the update method of the serializer """
        updated_data = {'username': 'updateduser', 'password': 'updatedpassword'}
        serializer = CustomUserSerializer(instance=self.user, data=updated_data, partial=True)

        # Ensure serializer is valid
        self.assertTrue(serializer.is_valid())

        # Call update to update the existing user
        updated_user = serializer.update(self.user, updated_data)

        # Ensure the existing user is updated with the provided data
        self.assertEqual(updated_user.username, 'updateduser')
