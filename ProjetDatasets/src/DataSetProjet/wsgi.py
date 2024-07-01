"""
Configuration WSGI pour le projet DataSetProjet.

Il expose l'appelable WSGI en tant que variable de module nommée ``application``.

Pour plus d'informations sur ce fichier, voir
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Définir le paramètre d'environnement pour spécifier le module de paramètres Django à utiliser
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataSetProjet.settings')

# Obtenir l'application WSGI pour le projet Django
application = get_wsgi_application()
