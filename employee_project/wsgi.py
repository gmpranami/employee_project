"""
WSGI config for employee_project.

This file exposes the WSGI callable as a module-level variable named ``application``.

WSGI (Web Server Gateway Interface) is the entry point for web servers
like Gunicorn or uWSGI to serve your Django project in production.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_project.settings')

application = get_wsgi_application()

# --- Auto-create superuser for Render deployment (silent) ---
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username="glynac").exists():
        User.objects.create_superuser(
            username="glynac",
            email="glynac@example.com",
            password="glynac"
        )
except Exception:
    pass
