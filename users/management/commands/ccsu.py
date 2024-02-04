from django.core.management.base import BaseCommand
from users.models import User
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('ADMIN_EMAIL'),
            first_name='Admin',
            last_name='Adminsky',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        user.set_password(os.getenv('ADMIN_PW'))
        user.save()
