"""
WSGI config for e-commerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


# set the default Django settings module for the  program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e-commerce.settings.development')



application = get_wsgi_application()
