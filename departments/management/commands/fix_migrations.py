from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Fix broken department migrations by removing stale records and re-creating tables."

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            # Check if table exists
            cursor.execute("""
                SELECT to_regclass('public.departments_department');
            """)
            exists = cursor.fetchone()[0]
            if exists:
                self.stdout.write(self.style.SUCCESS("✅ departments_department table already exists."))
                return

            # Drop migration record to force reapply
            cursor.execute("""
                DELETE FROM django_migrations WHERE app = 'departments';
            """)

            self.stdout.write(self.style.WARNING("⚠️ Deleted stale departments migration record."))
            self.stdout.write(self.style.SUCCESS("Next migration run will re-create the departments table."))
