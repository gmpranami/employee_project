#!/usr/bin/env python
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc

    args = sys.argv[:]
    is_migrate = len(args) >= 2 and args[1] == "migrate"
    auto_fix = os.environ.get("AUTO_FIX_MIGRATIONS", "1") == "1"

    if is_migrate and auto_fix:
        # --- Step 0: ensure employees depends on departments in code ---
        # Make sure employees/migrations/0001_initial.py has:
        # dependencies = [('departments', '0001_initial')]
        # (commit that change if it wasn't there)

        try:
            # Step A: logically unapply employees (no table drops)
            execute_from_command_line([args[0], "migrate", "employees", "zero", "--fake"])
        except Exception as e:
            print(f"[warn] Could not fake-unapply employees: {e}")

        try:
            # Step B: logically mark departments initial as applied (if tables exist)
            # If already applied, this is a no-op; if not, it marks it.
            execute_from_command_line([args[0], "migrate", "departments", "0001", "--fake"])
        except Exception as e:
            print(f"[warn] Could not fake-apply departments.0001: {e}")

        try:
            # Step C: now do a normal migrate (with --fake-initial for existing tables)
            execute_from_command_line([args[0], "migrate", "--noinput", "--fake-initial"])
            # Important: exit so the outer Render command doesn't run migrate again.
            sys.exit(0)
        except Exception as e:
            print(f"[fatal] Auto-fix migrate failed: {e}")
            # Fail fast so you can see the error
            sys.exit(1)

    # Default path (non-migrate commands, or auto-fix disabled)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
