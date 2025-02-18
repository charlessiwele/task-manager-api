import logging
from django.core.management import BaseCommand
from tm_api.services.user_generator import generate_user

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'GENERATE A DEFAULT STAFF USER'
    """
    This command is useful for generating the app's default staff user
    """

    def handle(self, *args, **options):
        try:
            print('Welcome to default staff user generator')
            logger.debug('Generating default staff user')
            username = 'staff'
            password = 'staff'
            user_email = 'staff@staff.staff'
            generated_staff_user = generate_user(username, password, user_email, is_staff = True)
            logger.debug('Generating default staff user completed successfully')
            print(f'Staff User Generated:\n username: {generated_staff_user.username} user_email: {generated_staff_user.email}, password: {generated_staff_user.password}')
        except Exception as exception:
            print(exception.__str__())