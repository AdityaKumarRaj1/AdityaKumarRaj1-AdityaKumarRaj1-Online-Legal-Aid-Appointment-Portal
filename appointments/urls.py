"""URL patterns for appointments app."""
from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.my_appointments, name='list'),
    path('book/<int:lawyer_id>/', views.book_appointment, name='book'),
    path('<int:pk>/', views.appointment_detail, name='detail'),
    path('<int:pk>/cancel/', views.cancel_appointment, name='cancel'),
    path('<int:appointment_id>/upload/', views.upload_document, name='upload_document'),
]
