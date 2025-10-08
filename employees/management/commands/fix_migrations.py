from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Fix inconsistent migration history"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_migrations WHERE app = 'employees';")
            cursor.execute("DELETE FROM django_migrations WHERE app = 'departments';")
        self.stdout.write(self.style.SUCCESS("✅ Migration history for employees and departments reset."))
