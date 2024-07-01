from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # Pour accéder a l'intterfaace d'administration de Django
    path('', include('DataSetsApp.urls')),  # Inclure les URL de l'application DataSetsApp
    path('accounts/', include('django.contrib.auth.urls')),  # Inclure les URL d'authentification
]