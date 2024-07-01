from django.urls import path
from . import views # Importation des vues depuis le fichier views.py


# On définit ici les routes (ou urlpatterns) pour notre application
urlpatterns = [
    path('upload/', views.upload_dataset, name='upload_dataset'), # Route pour uploader un dataset
    path('upload_images/', views.upload_image_folder, name='upload_image_folder'),
    path('datasets/', views.list_datasets, name='list_datasets'),
    path('', views.home, name='home'), # Route pour la page d'accueil
    path('signup/', views.signup, name='signup'),
    path('download_data/<str:collection_name>/<str:fichier_type>/', views.download_data, name='download_data'),
    path('download_all_images/<str:image_collection_name>/', views.download_all_images, name='download_all_images'),
]
