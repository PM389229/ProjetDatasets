from django.urls import path
from . import views # Importation des vues depuis le fichier views.py
from .views import download_chatbot_response

# On définit ici les routes (ou urlpatterns) pour notre application
urlpatterns = [
    path('upload/', views.upload_dataset, name='upload_dataset'), # Route pour uploader un dataset
    path('upload_images/', views.upload_image_folder, name='upload_image_folder'),
    path('datasets/', views.list_datasets, name='list_datasets'),
    path('', views.home, name='home'), # Route pour la page d'accueil
    path('signup/', views.signup, name='signup'),
    path('delete_image_folder/<str:folder_name>/', views.delete_image_folder, name='delete_image_folder'),
    path('delete_dataset/<str:dataset_id>/', views.delete_dataset, name='delete_dataset'),
    path('download_data/<str:collection_name>/<str:fichier_type>/', views.download_data, name='download_data'),
    path('download_all_images/<str:image_collection_name>/', views.download_all_images, name='download_all_images'),
    path('generate_dataset/', views.generate_dataset_view, name='generate_dataset'),
    path('view_dataset/', views.view_dataset_view, name='view_dataset'),
    path('download_chatbot_response/', download_chatbot_response, name='download_chatbot_response'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('download_json/', views.download_json, name='download_json'),
    path('convert_to_csv/', views.convert_to_csv, name='convert_to_csv'),
    path('convert_to_json/', views.convert_to_json, name='convert_to_json'),
]
