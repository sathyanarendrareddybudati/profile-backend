from django.urls import path
from .views import UserProfileAPIView, UserRegistrationAPI, UserLoginAPI
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('register/',UserRegistrationAPI.as_view(),name='registration'),
    path('login/',UserLoginAPI.as_view(),name='login'),
    path('api-token-auth/', obtain_auth_token),
]
