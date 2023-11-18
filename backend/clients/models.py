from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """ Default client class """
    pass

    def __str__(self):
        """ String representation """
        return self.username

    class Meta:
        """ Representation in admin panel """
        verbose_name = 'User'
        verbose_name_plural = 'Users'


