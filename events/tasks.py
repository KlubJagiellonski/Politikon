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
    skip_events = (
        tch.EVENT_CANCELLED_DEBIT_CHOICE.value,
        tch.EVENT_CANCELLED_REFUND_CHOICE.value,
        tch.EVENT_WON_PRIZE_CHOICE.value,
    )
    for event in Event.objects.filter(outcome=Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS):
        transactions = Transaction.objects.filter(date__gt=yesterday).exclude(type__in=skip_events)
        if transactions.exists():
            transaction = transactions[0]
            if transaction.type == tch.BUY_NO_CHOICE or transaction.type == tch.SELL_NO_CHOICE:
                value = Event.PRIZE_FOR_WINNING - transaction.price
            else:
                value = transaction.price
            price_change = value - event.price_change
            event.price_change = price_change
            event.absolute_price_change = abs(price_change)
            logger.debug(
                "'events:tasks:calculate_price_change' changing price_change of event "
                "<%s> to %s" % (unicode(event.pk), price_change)
            )
            event.save()
