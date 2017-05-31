import logging

from celery import task
from constance import config
from django.db import transaction
from django.db.models import Avg

from accounts.models import UserProfile, Team
from events.models import Transaction


logger = logging.getLogger(__name__)


@task
def topup_accounts_task():
    """
    Daily topup accounts task
    """
    logger.debug("'politikon:tasks:topup_accounts_task' worker up")
    topup_amount = config.DAILY_TOPUP

    for user in UserProfile.objects.get_users().iterator():
        try:
            with transaction.atomic():
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

    for user in UserProfile.objects.get_users().only('id', 'portfolio_value', 'reset_date').\
            iterator():
        portfolio_value = user.current_portfolio_value
        if user.portfolio_value != portfolio_value:
            user.portfolio_value = portfolio_value
            user.save(update_fields=['portfolio_value'])

    logger.debug("'accounts:tasks:update_portfolio_value' finished.")


@task
def update_teams_score():
    """
    Update teams score
    """
    logger.debug("'accounts:tasks:update_teams_score' worker up")

    for team in Team.objects.all():
        team.avg_reputation = UserProfile.objects.filter(team=team).\
            aggregate(Avg('reputation'))['reputation__avg']
        team.avg_total_cash = UserProfile.objects.filter(team=team).\
            aggregate(Avg('total_cash'))['total_cash__avg']
        team.avg_portfolio_value = UserProfile.objects.filter(team=team).\
            aggregate(Avg('portfolio_value'))['portfolio_value__avg']
        team.avg_weekly_result = UserProfile.objects.filter(team=team).\
            aggregate(Avg('weekly_result'))['weekly_result__avg']
        team.avg_monthly_result = UserProfile.objects.filter(team=team).\
            aggregate(Avg('monthly_result'))['monthly_result__avg']
        team.save()


@task
def create_accounts_snapshot():
    logger.debug("'accounts:tasks:create_accounts_snapshot' worker up")

    queryset = UserProfile.objects.all()

    for user in queryset.iterator():
        try:
            logger.debug("'accounts:tasks:create_accounts_snapshot' snapshotting user <%s>" % unicode(user.pk))
            user.snapshots.create_snapshot()
        except:
            logger.exception("Fatal error during create_accounts_snapshot of user #%d" % (user.id,))

    logger.debug("'accounts:tasks:create_accounts_snapshot' finished snapshotting Users.")


@task
def update_users_last_transaction():
    """
    Update users last transaction date.
    """
    for user in UserProfile.objects.get_users().iterator():
        transactions = Transaction.objects.filter(user=user, type__in=Transaction.BUY_SELL_TYPES).\
            order_by('-date')[:1]
        if len(transactions):
            user.last_transaction = transactions[0].date
            user.save()


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
