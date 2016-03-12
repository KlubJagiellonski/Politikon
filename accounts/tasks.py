from collections import defaultdict
import logging

from celery import task
from constance import config
from django.db import transaction

from accounts.models import UserProfile
from events.models import Bet, Event, Transaction

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
    ???
    """
    logger.debug("'accounts:tasks:update_portfolio_value' worker up")

    users_value = defaultdict(float)

    queryset = Bet.objects.select_related('event').\
        filter(event__outcome=Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS)
    for bet in queryset.iterator():
        price_field = "current_sell_for_price"
        if bet.outcome is False:
            price_field = "current_sell_against_price"

        users_value[bet.user_id] += bet.has * getattr(bet.event, price_field)

    logger.debug("'accounts:tasks:update_portfolio_value' setting 0 value portfolios.")
    UserProfile.objects.all().\
        exclude(portfolio_value=0., id__in=users_value.keys()).\
        update(portfolio_value=0.)

    logger.debug(
        "'accounts:tasks:update_portfolio_value' updating portfolios value for %d users."
        % len(users_value)
    )
    for user_id, user_value in users_value.iteritems():
        UserProfile.objects.filter(id=user_id) \
                    .exclude(portfolio_value=user_value) \
                    .update(portfolio_value=user_value)

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
def update_weekly_result():
    tch = Transaction.TRANSACTION_TYPE_CHOICES
    income_transactions = (
        tch.SELL_YES,
        tch.SELL_NO,
        tch.EVENT_CANCELLED_REFUND_CHOICE,
        tch.EVENT_WON_PRIZE_CHOICE,
    )
    debit_transactions = (
        tch.BUY_YES,
        tch.BUY_NO,
        tch.EVENT_CANCELLED_DEBIT_CHOICE,
    )
    result = 0
    for user in UserProfile.objects.get_users():
        for t in Transaction.objects.get_weekly_user_transactions(user):
            if t in income_transactions:
                result += t.price
            elif t in debit_transactions:
                result -= t.price
        user.weekly_result = result
        user.save()


@task
def update_monthly_result():
    tch = Transaction.TRANSACTION_TYPE_CHOICES
    income_transactions = (
        tch.SELL_YES,
        tch.SELL_NO,
        tch.EVENT_CANCELLED_REFUND_CHOICE,
        tch.EVENT_WON_PRIZE_CHOICE,
    )
    debit_transactions = (
        tch.BUY_YES,
        tch.BUY_NO,
        tch.EVENT_CANCELLED_DEBIT_CHOICE,
    )
    result = 0
    for user in UserProfile.objects.get_users():
        for t in Transaction.objects.get_weekly_user_transactions(user):
            if t in income_transactions:
                result += t.price
            elif t in debit_transactions:
                result -= t.price
        user.weekly_result = result
        user.save()
