from datetime import timedelta
import logging

from celery import task
from django.utils.timezone import now

from .models import Event, Transaction


logger = logging.getLogger(__name__)


@task
def create_open_events_snapshot():
    """
    Create snapshot of events for time charts
    """
    logger.debug("'events:tasks:create_open_events_snapshot' worker up")

    for event in Event.objects.filter(outcome=Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS):
        try:
            logger.debug(
                "'events:tasks:create_open_events_snapshot' snapshotting event"
                " <%s>" % unicode(event.pk)
            )
            event.snapshots.create_snapshot()
        except:
            logger.exception(
                "Fatal error during create_open_events_snapshot of event"
                " #%d" % (event.id,)
            )

    logger.debug("'events:tasks:create_open_events_snapshot' finished snapshotting Events.")


@task
def calculate_price_change():
    """
    Calculate price change for events every day
    """
    logger.debug("'events:tasks:calculate_price_change' worker up")
    yesterday = now() - timedelta(days=1)
    for event in Event.objects.ongoing_only_queryset():
        snapshots = event.snapshots.filter(
            snapshot_of_id=event.id,
            created_at__lte=yesterday,
        ).order_by('-created_at')[:1]
        if snapshots.exists():
            last_price = snapshots[0].current_buy_for_price
        else:
            last_price = 50

        event.price_change = last_price - event.current_buy_for_price
        event.absolute_price_change = abs(event.price_change)
        event.save()
