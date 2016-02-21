from celery import task

import logging
logger = logging.getLogger(__name__)


@task
def create_open_events_snapshot():
    logger.debug("'events:tasks:create_open_events_snapshot' worker up")
    from .models import Event, EVENT_OUTCOMES_DICT

    queryset = Event.objects.filter(outcome=EVENT_OUTCOMES_DICT['IN_PROGRESS'])

    for event in queryset.iterator():
        try:
            logger.debug("'events:tasks:create_open_events_snapshot' \
                         snapshotting event <%s>" % unicode(event.pk))
            event.snapshots.create_snapshot()
        except:
            logger.exception("Fatal error during create_open_events_snapshot \
                             of event #%d" % (event.id,))

    logger.debug("'events:tasks:create_open_events_snapshot' finished \
                 snapshotting Events.")
