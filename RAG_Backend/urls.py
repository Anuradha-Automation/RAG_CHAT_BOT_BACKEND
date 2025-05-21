"""
URL configuration for RAG_Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from RAG_Backend import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # Uncomment the line below if you want to redirect the root URL to '/login/'
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    # Main application URLs
    path("", include("RAG_CHATBOT_BACKEND_APIS.urls")),
    path("api/v2/", include("RAG_CHATBOT_BACKEND_APIS.api_routes")),
    path('sonar/', include('django_sonar.urls')),
]


if settings.DEBUG:
    urlpatterns += settings.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += settings.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)