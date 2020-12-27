from .dev import *

SESSION_ENGINE = 'django.contrib.sessions.backends.file'  # makes assertNumQueries easier bc no queries for sessions
