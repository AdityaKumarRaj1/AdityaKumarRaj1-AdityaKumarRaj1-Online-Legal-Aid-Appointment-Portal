"""URL patterns for the accounts app."""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_citizen, name='register_citizen'),
    path('register/lawyer/', views.register_lawyer, name='register_lawyer'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
