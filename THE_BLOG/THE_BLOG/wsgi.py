"""
WSGI config for THE_BLOG project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
# changed to double refrence

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'THE_BLOG.settings')

application = get_wsgi_application()
