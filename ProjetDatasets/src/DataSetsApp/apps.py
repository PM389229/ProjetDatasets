from django.apps import AppConfig

# Définition de la configuration pour mon application 'DataSetsApp'.

class DatasetsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'     # type de champ de clé primaire par défaut pour les modèles de l'application
    name = 'DataSetsApp'

# Methode 'ready' appelé automatiquement sur Django quand l'appli est prete a etre utilisée
    def ready(self):
        import DataSetsApp.signals

