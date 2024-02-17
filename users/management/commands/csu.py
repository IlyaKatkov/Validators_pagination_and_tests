from django.core.management import BaseCommand
from users.models import User
class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@almaz25.pro',
            first_name='almaz',
            last_name='skyPro',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('12345678')
        user.save()