"""
WSGI config for bird_identification_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bird_identification_web.settings')

application = get_wsgi_application()

from accounts.wsgi import check_password
from django.contrib.auth.handlers.modwsgi import groups_for_user
