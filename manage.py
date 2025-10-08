#!/usr/bin/env python
import os
import sys
from django.core.management import execute_from_command_line
from django.db import connection


def main():
    """Entry point for Django manage commands."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "employee_project.settings")

    # --- TEMP FIX for inconsistent migration history ---
    if os.environ.get("RENDER") == "1":
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM django_migrations
                    WHERE app IN ('employees', 'departments', 'attendance');
                """)
            print("✅ Cleared inconsistent migration history for employees, departments, and attendance.")
        except Exception as e:
            print(f"⚠️ Migration cleanup skipped: {e}")
    # ---------------------------------------------------

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
