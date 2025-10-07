from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Resets all migration history and rebuilds a clean database."

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_migrations;")
        self.stdout.write(self.style.SUCCESS("✅ Migration history reset. Run migrate next."))
