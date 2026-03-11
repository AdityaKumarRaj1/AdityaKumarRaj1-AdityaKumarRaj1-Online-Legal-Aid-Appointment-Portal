"""REST API URL patterns for accounts."""
from django.urls import path
from . import api_views

urlpatterns = [
    path('auth/register/', api_views.UserRegistrationAPIView.as_view(), name='api_register'),
    path('auth/profile/', api_views.UserProfileAPIView.as_view(), name='api_profile'),
    path('users/', api_views.UserListAPIView.as_view(), name='api_users'),
]
