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
        portfolio_value = 0
        # get all user bets for not resolved events and has > 0
        for bet in user.bets.filter(has__gt=0).select_related('event').filter(
            event__outcome=Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS,
        ).iterator():
            if bet.outcome is False:
                portfolio_value += bet.has * getattr(bet.event, "current_sell_against_price")
            elif bet.outcome:
                portfolio_value += bet.has * getattr(bet.event, "current_sell_for_price")
        if user.portfolio_value != portfolio_value:
            user.save(portfolio_value=portfolio_value)

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
    for user in UserProfile.objects.get_users().iterator():
        weekly_result = 0
        for t in Transaction.objects.get_weekly_user_transactions(user).iterator():
            if t in income_transactions:
                weekly_result += t.price
            elif t in debit_transactions:
                weekly_result -= t.price

        monthly_result = 0
        for t in Transaction.objects.get_monthly_user_transactions(user).iterator():
            if t in income_transactions:
                monthly_result += t.price
            elif t in debit_transactions:
                monthly_result -= t.price

        if user.weekly_result != weekly_result or user.monthly_result != monthly_result:
            user.save(weekly_result=weekly_result, monthly_result=monthly_result)
