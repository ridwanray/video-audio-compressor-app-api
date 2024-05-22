"""
ASGI config for Compressor project.
"""

import os
from decouple import config
from django.core.asgi import get_asgi_application

environment = config('ENVIRONMENT')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings."+environment)


application = get_asgi_application()
