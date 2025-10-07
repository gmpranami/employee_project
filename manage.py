#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_project.settings')
    from django.core.management import execute_from_command_line

    args = sys.argv
    # If Render is calling `manage.py migrate` and we can't run it safely, skip it.
    if len(args) >= 2 and args[1] == "migrate" and os.environ.get("SKIP_MIGRATE_ON_RENDER") == "1":
        print("[info] SKIP_MIGRATE_ON_RENDER=1 -> skipping migrate step on Render")
        sys.exit(0)

    execute_from_command_line(args)

if __name__ == '__main__':
    main()
