import logging
from tm_api.models import Status

logger = logging.getLogger(__name__)


def generate_statuses(statuses = []):
    generated_statuses = []
    try:
        logger.debug('Generating default statuses')
        for status in statuses:
            generated_status, created = Status.objects.get_or_create(
                name=status,
                description=status
            )
            generated_statuses.append(generated_status)
            print(f'Status {status} generated')
            logger.debug(f'Status {status} generated')
        logger.debug('Generating default statuses completed successfully')
        return generated_statuses
    except Exception as exception:
        print(exception.__str__())