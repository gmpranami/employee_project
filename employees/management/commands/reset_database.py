from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Drops all tables and rebuilds a clean database schema."

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("""
                DO $$
                DECLARE
                    rec RECORD;
                BEGIN
                    FOR rec IN
                        (SELECT tablename FROM pg_tables WHERE schemaname = 'public')
                    LOOP
                        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(rec.tablename) || ' CASCADE';
                    END LOOP;
                END $$;
            """)
        self.stdout.write(self.style.SUCCESS("✅ All tables dropped successfully. Run migrate next."))
