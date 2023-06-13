from django.urls import path
from .views import UserProfileAPIView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('api-token-auth/', obtain_auth_token),
]
