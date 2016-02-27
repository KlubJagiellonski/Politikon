from datetime import datetime, timedelta
import logging

from celery import task


logger = logging.getLogger(__name__)


@task
def create_open_events_snapshot():
    logger.debug("'events:tasks:create_open_events_snapshot' worker up")
    from .models import Event

    for event in Event.objects.in_progress():
        try:
            logger.debug("'events:tasks:create_open_events_snapshot' snapshotting event <%s>" % unicode(event.pk))
            event.snapshots.create_snapshot()
        except:
            logger.exception("Fatal error during create_open_events_snapshot of event #%d" % (event.id,))

    logger.debug("'events:tasks:create_open_events_snapshot' finished snapshotting Events.")


@task
def calculate_price_change():
    logger.debug("'events:tasks:calculate_price_change' worker up")
    from .models import Event, Translation

    for event in Event.objects.in_progress():
        yesterday = datetime.today() - timedelta(1)
        skip_events = (
            tch.EVENT_CANCELLED_DEBIT_CHOICE.value,
            tch.EVENT_CANCELLED_REFUND_CHOICE.value,
            tch.EVENT_WON_PRIZE_CHOICE.value,
        )
        transactions = Transaction.objects.filter(date__gt=yesterday).\
            exclude(type__in=skip_events)
        if len(transactions) > 0:
            t = transactions[0]
            if t.type == tch.BUY_NO_CHOICE or \
                    t.type == tch.SELL_NO_CHOICE:
                value = 100-t.price
            else:
                value = t.price
            price_change = value - event.price_change
            event.price_change = price_change
            event.absolute_price_change = abs(price_change)
            logger.debug("'events:tasks:calculate_price_change' changing price_change of event <%s> to %s" % (unicode(event.pk), price_change))
            event.save()
