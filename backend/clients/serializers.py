from rest_framework import serializers
from clients.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """ Serializer for the CustomUser model """

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password')
