"""URL patterns for dashboard app."""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('citizen/', views.citizen_dashboard, name='citizen_dashboard'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', views.admin_manage_users, name='admin_manage_users'),
    path('admin-panel/lawyers/<int:lawyer_id>/verify/',
         views.admin_verify_lawyer, name='admin_verify_lawyer'),
    path('admin-panel/categories/', views.admin_manage_categories,
         name='admin_manage_categories'),
    path('admin-panel/appointments/', views.admin_all_appointments,
         name='admin_all_appointments'),
]
