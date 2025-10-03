"""
WSGI config for employee_project.

This file exposes the WSGI callable as a module-level variable named ``application``.

WSGI (Web Server Gateway Interface) is the entry point for web servers
like Gunicorn or uWSGI to serve your Django project in production.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for WSGI deployment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "employee_project.settings")

# The WSGI application object used by WSGI servers
application = get_wsgi_application()
