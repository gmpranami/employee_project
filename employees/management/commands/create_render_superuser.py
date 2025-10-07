from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Creates the default Render superuser (glynac)."

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="glynac").exists():
            User.objects.create_superuser(
                username="glynac",
                email="glynac@example.com",
                password="glynac"
            )
            self.stdout.write(self.style.SUCCESS("Superuser 'glynac' created."))
        else:
            self.stdout.write(self.style.WARNING("Superuser 'glynac' already exists."))
