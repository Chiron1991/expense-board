from .prod import *

DEBUG = True

SECRET_KEY = os.getenv('SECRET_KEY', 'superSECRET123')

ALLOWED_HOSTS = []

INTERNAL_IPS = ['127.0.0.1']  # required by debug_toolbar

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
