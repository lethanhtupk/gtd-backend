from .base import *
import dj_database_url
from dj_database_url import config

DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
