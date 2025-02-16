import logging
from tm_api.services.user_generator import generate_user
from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'GENERATE A SUPERUSER'
    """
    This command is useful for generating the app's default superuser
    """

    def handle(self, *args, **options):
        try:
            print('Welcome to default superuser generator')
            username = 'admin'
            password = 'admin'
            user_email = f'{username}@{username}.{username[:2]}'
            generated_staff_user = generate_user(username, password, user_email, is_staff = True, is_superuser=True)
            print(f'Superuser Generated:\n username: {generated_staff_user.username} user_email: {generated_staff_user.user_email}, password: {generated_staff_user.password}')
        except Exception as exception:
            print(exception.__str__())