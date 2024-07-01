"""
Configuration ASGI pour le projet DataSetProjet.

Il expose l'appelable ASGI en tant que variable de niveau module nommée ``application``.


For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataSetProjet.settings')

application = get_asgi_application()
