from datetime import timedelta
import logging

from celery import task
from django.utils.timezone import now

from .models import Event, Transaction


logger = logging.getLogger(__name__)


@task
def create_open_events_snapshot():
    """
    ???
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
    tch = Transaction.TRANSACTION_TYPE_CHOICES
    transaction_types = (
        tch.BUY_YES,
        tch.SELL_YES,
        tch.BUY_NO,
        tch.SELL_NO,
    )
    for event in Event.objects.filter(outcome=Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS):
        transactions = Transaction.objects.filter(
            event=event,
            date__lte=yesterday,
            type__in=transaction_types,
        ).order_by('-date')[:1]

        if transactions.exists():
            transaction = transactions[0]
            if transaction.type == tch.BUY_NO:
                event.price_change = event.current_buy_against_price - transaction.price
            elif transaction.type == tch.SELL_NO:
                event.price_change = event.current_sell_against_price - transaction.price
            elif transaction.type == tch.BUY_YES:
                event.price_change = event.current_buy_for_price - transaction.price
            elif transaction.type == tch.SELL_YES:
                event.price_change = event.current_sell_for_price - transaction.price
            event.absolute_price_change = abs(event.price_change)
            logger.debug(
                "'events:tasks:calculate_price_change' changing price_change of event "
                "<%s> to %s" % (unicode(event.pk), event.price_change)
            )
            event.save()
