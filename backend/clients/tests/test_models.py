from django.test import TestCase

from clients.models import CustomUser


class CustomUserModelTest(TestCase):
    def setUp(self):
        """ Create a test user """
        self.user = CustomUser.objects.create(username='testuser', password='testpassword')

    def test_str_method(self):
        """ Test the __str__ method of the model """
        self.assertEqual(str(self.user), 'testuser')

    def test_verbose_name_plural(self):
        """ Test the verbose_name_plural attribute in the Meta class """
        self.assertEqual(CustomUser._meta.verbose_name_plural, 'Users')

    def test_verbose_name(self):
        """ Test the verbose_name attribute in the Meta class """
        self.assertEqual(CustomUser._meta.verbose_name, 'User')
