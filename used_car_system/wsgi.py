"""
WSGI config for used_car_system project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'used_car_system.settings')

application = get_wsgi_application()