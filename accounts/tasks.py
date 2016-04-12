import logging

from celery import task
from constance import config
from django.db import transaction

from accounts.models import UserProfile
from events.models import Event, Transaction

logger = logging.getLogger(__name__)


@task
def topup_accounts_task():
    """
    ???
    """
    logger.debug("'politikon:tasks:topup_accounts_task' worker up")
    topup_amount = config.DAILY_TOPUP

    with transaction.atomic():
        for user in UserProfile.objects.all().iterator():
            try:
                user.topup_cash(topup_amount)
            except:
                logger.exception("Fatal error during topping up of user \
                                 #%d <%s>" % (user.id, user))


@task
def update_portfolio_value():
    """
    Update all users portfolio_value
    """
    logger.debug("'accounts:tasks:update_portfolio_value' worker up")

    for user in UserProfile.objects.get_users().iterator():
        portfolio_value = user.current_portfolio_value
        if user.portfolio_value != portfolio_value:
            user.portfolio_value = portfolio_value
            user.save()

    logger.debug("'accounts:tasks:update_portfolio_value' finished.")


@task
def create_accounts_snapshot():
    logger.debug("'accounts:tasks:create_accounts_snapshot' worker up")

    queryset = UserProfile.objects.all()

    for user in queryset.iterator():
        try:
            logger.debug("'accounts:tasks:create_accounts_snapshot' \
                         snapshotting user <%s>" % unicode(user.pk))
            user.snapshots.create_snapshot()
        except:
            logger.exception("Fatal error during create_accounts_snapshot of \
                             user #%d" % (user.id,))

    logger.debug("'accounts:tasks:create_accounts_snapshot' finished \
                 snapshotting Users.")


@task
def update_users_classification():
    """
    Update weekly and monthly users classifications.
    """
    for user in UserProfile.objects.get_users().iterator():
        weekly_result = user.get_last_week_reputation_change()
        monthly_result = user.get_last_month_reputation_change()

        if user.weekly_result != weekly_result or user.monthly_result != monthly_result:
            user.weekly_result = weekly_result
            user.monthly_result = monthly_result
            user.save(update_fields=['weekly_result', 'monthly_result'])
