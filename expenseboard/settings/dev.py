from .prod import *

DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = ['127.0.0.1']  # required by debug_toolbar

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
