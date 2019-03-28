import os
import raven

from .base import *


ALLOWED_HOSTS += [os.getenv('DOMAIN_NAME')]

# Sentry
INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]
RAVEN_CONFIG = {
    'dsn': os.getenv('RAVEN_DSN'),
}

# HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
