from django.urls import path
from clients import views

urlpatterns = [
    # URL for creating a new user
    path('create_user/', views.CreateUserAPIView.as_view(), name='create_user'),

    # URL for retrieving, updating, and deleting users
    path('users/', views.UserAPIView.as_view(), name='user_list'),
    path('users/<int:user_id>/', views.UserAPIView.as_view(), name='user_detail'),
]
