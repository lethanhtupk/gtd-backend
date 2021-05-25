from .base import *
import dj_database_url
from dj_database_url import config

DEBUG = False

# this is the domain name for above ACTIVATION_URL
DOMAIN = "get-the-deal.web.app"

ALLOWED_HOSTS = ['gtd-api.herokuapp.com', '127.0.0.1']

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
