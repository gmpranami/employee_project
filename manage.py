#!/usr/bin/env python
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django."
        ) from exc

    # ------------------------------------------------------------
    # AUTO-FIX for InconsistentMigrationHistory on Render
    # Runs ONLY when the command is 'migrate'.
    # It fakes employees back to zero so departments can apply first.
    # You can disable by setting AUTO_FIX_MIGRATIONS=0 in env.
    # ------------------------------------------------------------
    args = sys.argv[:]
    if len(args) >= 2 and args[1] == "migrate" and os.environ.get("AUTO_FIX_MIGRATIONS", "1") == "1":
        try:
            # 1) logically unapply employees to clear wrong order
            execute_from_command_line([args[0], "migrate", "employees", "zero", "--fake"])
        except Exception as e:
            print(f"[warn] Pre-fix (fake unapply employees) failed: {e}")

        try:
            # 2) apply everything; --fake-initial helps if tables already exist
            execute_from_command_line([args[0], "migrate", "--noinput", "--fake-initial"])
            return  # we're done; avoid a second migrate call below
        except Exception as e:
            print(f"[warn] Main migrate (with --fake-initial) failed, falling back: {e}")

    # Normal execution for all other commands
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
