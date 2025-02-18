import logging
from django.core.management import BaseCommand
from tm_api.services.user_generator import generate_user

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'GENERATE A DEFAULT Generic USER'
    """
    This command is useful for generating the app's default generic user
    """

    def handle(self, *args, **options):
        try:
            print('Welcome to default generic user generator')
            logger.debug('Generating default generic user')
            username = 'generic'
            password = 'generic'
            user_email = 'generic@generic.generic'
            generated_staff_user = generate_user(username, password, user_email)
            print(f'Generic User Generated:\n username: {generated_staff_user.username} user_email: {generated_staff_user.email}, password: {generated_staff_user.password}')
            logger.debug('Default generic user generated successfully')
        except Exception as exception:
            print(exception.__str__())