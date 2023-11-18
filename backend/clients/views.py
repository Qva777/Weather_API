from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from clients.models import CustomUser
from clients.serializers import CustomUserSerializer


class CreateUserAPIView(APIView):
    """ View for creating a new user """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        """ GET requests for user information """
        if user_id:
            user = self.get_user(user_id)
            if isinstance(user, Response):
                return user
            serializer = CustomUserSerializer(user)
        else:
            users = CustomUser.objects.all()
            serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        """ PUT requests for updating user information """
        user = self.get_user(user_id)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():

            new_password = serializer.validated_data.get('password')
            if new_password:
                serializer.validated_data['password'] = make_password(new_password)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        """ DELETE requests for deleting a user """
        user = self.get_user(user_id)

        if isinstance(user, Response):
            return user

        user.delete()
        return Response({"detail": "User successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_user(user_id):
        """ Retrieve a user by ID """
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid user ID'}, status=status.HTTP_404_NOT_FOUND)
