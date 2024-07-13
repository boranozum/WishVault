PROJECT_APPS = [
    'account',
    'product',
]

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_password_validators',
    'django_password_validators.password_history',
    'django_filters'
] + PROJECT_APPS

