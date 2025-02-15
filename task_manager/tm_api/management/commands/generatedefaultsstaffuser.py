import logging
import pathlib
import random
import string
from django.contrib.auth.models import User
from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'GENERATE A STAFF USER'
    """
    This command is useful for generating the app's default staff
    """

    def handle(self, *args, **options):
        try:
            print('Welcome to default staff user generator')
            username = 'staff'
            password = 'staff'
            user_email = f'{username}@{username}.{username[:2]}'
            user = User.objects.create_superuser(username, user_email, password)
            user.is_superuser = False
            user.save()
            print(f'Staff User Generated:\n username: {username} user_email: {user_email}, password: {password}')
        except Exception as exception:
            print(exception.__str__())