from django.core.management.base import BaseCommand
from django.utils.timezone import now

from constance import config

from accounts.models import UserProfile
from accounts.tasks import (
    update_portfolio_value, update_users_last_transaction, update_users_classification
)


class Command(BaseCommand):
    help = 'Resets all accounts and ongoing events results'

    def handle(self, *args, **options):
        update_portfolio_value()
        update_users_last_transaction()
        for u in UserProfile.objects.get_users():
            u.reset_date = now()
            u.topup_cash(config.STARTING_CASH - (u.total_cash + u.portfolio_value))
            u.save()
        update_users_classification()
