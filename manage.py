#!/usr/bin/env python
"""
Django’s command-line utility for administrative tasks.

This script is the main entry point for running management commands such as:
- runserver: start the development server
- makemigrations/migrate: manage database migrations
- createsuperuser: create an admin user
- custom commands (e.g., seed_data)

It ensures Django settings are loaded before executing the requested command.
"""

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "employee_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed "
            "and available on your PYTHONPATH environment variable? "
            "Did you forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
