from .base import *
import os

DEBUG = True

# this is the domain name for above ACTIVATION_URL
DOMAIN = "localhost:3000"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
