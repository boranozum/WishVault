from os import path

ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = 'wishvault.urls'

WSGI_APPLICATION = 'wishvault.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True

SETTINGS_PATH = path.dirname(path.abspath(__file__))
