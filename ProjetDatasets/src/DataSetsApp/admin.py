from django.contrib import admin  # Importation du module d'administration de Django
from .models import Dataset, Image  # Importation des modèles que vous l'on veut enregistrer dans la partie administration

# Enregistrement des modèles dans l'interface d'administration de Django
# Cela permet de gérer les instances des modèles via l'interface d'administration (connexion avec SuperUser)

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'fichier_type', 'uploaded_by', 'uploaded_at')  # Colonnes à afficher dans la liste des datasets
    search_fields = ('titre',)  # Champs par lesquels on peut effectuer une recherche
    list_filter = ('fichier_type', 'uploaded_at')  # Filtres disponibles dans la liste de nos datasets

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_name', 'uploaded_by', 'uploaded_at')  # Colonnes à afficher dans la liste des images
    search_fields = ('image_name',)  
    list_filter = ('uploaded_at',) 
