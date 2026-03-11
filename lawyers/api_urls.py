"""REST API URL patterns for lawyers."""
from django.urls import path
from . import api_views

urlpatterns = [
    path('lawyers/', api_views.LawyerListAPIView.as_view(), name='api_lawyer_list'),
    path('lawyers/<int:pk>/', api_views.LawyerDetailAPIView.as_view(), name='api_lawyer_detail'),
]
