"""URL patterns for lawyers app."""
from django.urls import path
from . import views

app_name = 'lawyers'

urlpatterns = [
    path('', views.lawyer_list, name='list'),
    path('dashboard/', views.lawyer_dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('availability/', views.manage_availability, name='availability'),
    path('availability/<int:pk>/delete/', views.delete_availability, name='delete_availability'),
    path('<int:pk>/', views.lawyer_detail, name='detail'),
    path('appointment/<int:appointment_id>/<str:action>/',
         views.appointment_action, name='appointment_action'),
]
