"""
WSGI config for LookingForConcerts project.

It exposes the WSGI callable as a module-level variable named ``application``.
(Helps our Django application to communicate with the web server.)

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LookingForConcerts.settings")

application = get_wsgi_application()
