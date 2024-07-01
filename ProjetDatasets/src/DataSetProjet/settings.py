from pathlib import Path
import os

# Construction des chemins à l'intérieur du projet comme ceci : BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Paramètres de démarrage rapide pour le développement - inadaptés à la production

# AVERTISSEMENT DE SÉCURITÉ : gardez la clé secrète utilisée en production secrète !

SECRET_KEY = 'django-insecure-e@$=-8r%@0y!oe=rpeyqrffi3=g7^zi2n&2v%t_xnjxbqn0+0#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Définition des applications

INSTALLED_APPS = [
    # Applis django par defaut 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Mes Applis personnalisées
    'rest_framework',
    'DataSetsApp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DataSetProjet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DataSetProjet.wsgi.application'

# BDD

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'my_database': {
        'ENGINE': 'djongo',
        'NAME': 'my_database',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': '127.0.0.1',
            'port': 27017,
            'username': 'PM929',
            'password': 'root',
            'authSource': 'admin',
            'authMechanism': 'SCRAM-SHA-1',
        },
    },
    'my_database_images': {
        'ENGINE': 'djongo',
        'NAME': 'my_database_images',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': '127.0.0.1',
            'port': 27017,
            'username': 'PM929',
            'password': 'root',
            'authSource': 'admin',
            'authMechanism': 'SCRAM-SHA-1',
        },
    }
}

# routeurs de BDD
DATABASE_ROUTERS = ['DataSetProjet.database_router.DatabaseRouter']

# URL de redirection après la connexion
LOGIN_REDIRECT_URL = 'list_datasets'
LOGOUT_REDIRECT_URL = 'login'

# Validation des mots de passe

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Taille maximale d'un seul fichier en octets
DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400  # 25 MB

# Taille totale maximale de la requête en octets
FILE_UPLOAD_MAX_MEMORY_SIZE = 26214400  # 25 MB

# Nombre maximal de fichiers pouvant être téléchargés
DATA_UPLOAD_MAX_NUMBER_FILES = 100  # qu'on peut ajuster




# Static (CSS, JavaScript, Images)


STATIC_URL = 'static/'
APPEND_SLASH = True 

# Type de champ de clé primaire par défaut


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'