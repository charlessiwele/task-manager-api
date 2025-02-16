import logging
from django.core.management import BaseCommand
from tm_api.services.user_generator import generate_user
import string
import secrets


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'GENERATE A DJANGO SECRET'
    """
    This command is useful for generating the app's Django Secret Key
    """

    def handle(self, *args, **options):
        try:
            print('Welcome to Django secret key generator')
            c = string.ascii_letters + string.digits + string.punctuation
            secret_key = ''.join(secrets.choice(c) for i in range(67))
            print(f'Generated Key: {secret_key}')
        except Exception as exception:
            print(exception.__str__())