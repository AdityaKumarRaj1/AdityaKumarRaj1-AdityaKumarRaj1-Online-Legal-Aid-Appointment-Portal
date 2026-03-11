"""REST API URL patterns for appointments."""
from django.urls import path
from . import api_views

urlpatterns = [
    path('appointments/', api_views.AppointmentListAPIView.as_view(),
         name='api_appointment_list'),
    path('appointments/create/', api_views.AppointmentCreateAPIView.as_view(),
         name='api_appointment_create'),
    path('appointments/<int:pk>/', api_views.AppointmentDetailAPIView.as_view(),
         name='api_appointment_detail'),
    path('appointments/<int:pk>/status/', api_views.AppointmentStatusUpdateAPIView.as_view(),
         name='api_appointment_status'),
]
