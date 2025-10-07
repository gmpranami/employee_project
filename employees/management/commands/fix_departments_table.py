from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Force recreate departments table if missing."

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departments_department (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT
                );
            """)
        self.stdout.write(self.style.SUCCESS("✅ Departments table ensured."))
