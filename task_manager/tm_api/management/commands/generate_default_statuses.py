import logging
from tm_api.services.status_generator import generate_statuses
from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'GENERATE DEFAULT STATUSES'
    """
    This command is for generating default statuses
    """

    def handle(self, *args, **options):
        try:
            print('Welcome to default statuses generator')
            logger.debug('Generating default statuses')
            statuses = ['PENDING', 'IN_PROGRESS', 'COMPLETED']
            generate_statuses(statuses)
            logger.debug('Generating default staff user completed successfully')
            print(f'All default statuses generated!')
        except Exception as exception:
            print(exception.__str__())