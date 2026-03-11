"""
URL Configuration for legal_aid_portal project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('lawyers/', include('lawyers.urls')),
    path('appointments/', include('appointments.urls')),
    path('categories/', include('categories.urls')),
    path('dashboard/', include('dashboard.urls')),
    # REST API
    path('api/', include('accounts.api_urls')),
    path('api/', include('lawyers.api_urls')),
    path('api/', include('appointments.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
