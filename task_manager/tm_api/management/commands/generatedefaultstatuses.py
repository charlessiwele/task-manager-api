import logging
from tm_api.models import Status
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
            statuses = ['PENDING', 'IN_PROGRESS', 'COMPLETED']
            for status in statuses:
                Status.objects.get_or_create(
                    name=status,
                    description=status
                )
                print(f'Status {status} generated')
            print(f'All default statuses generated!')
        except Exception as exception:
            print(exception.__str__())