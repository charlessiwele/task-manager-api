import logging
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def generate_user(username, password, user_email, is_superuser = False, is_staff = False):
    try:
        logger.debug(f'Generating user {username}')
        user_email = f'{username}@{username}.{username[:2]}'
        user = User.objects.create_superuser(username, user_email, password)
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.save()
        logger.debug(f'User {username} generated successfully')
        return user
    except Exception as exception:
        print(exception.__str__())