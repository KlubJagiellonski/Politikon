from django.core.management.base import BaseCommand, CommandError

from datetime import timedelta
from events.models import Transaction, Bet, Event
from accounts.models import UserProfile
from constance import config
from django.utils.timezone import now


class Command(BaseCommand):
    def handle(self, *args, **options):
        for t in Transaction.objects.filter(type=Transaction.TRANSACTION_TYPE_CHOICES.TOPPED_UP_BY_APP):
            t.delete()

        for b in Bet.objects.filter(event__outcome=Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS):
            b.delete()

        for e in Event.objects.ongoing_only_queryset():
            e.quantity = 0
            e.Q_against = e.Q_for = 0
            e.save()
            e.recalculate_prices()

        for u in UserProfile.objects.get_users():
            u.active_date = now()
            u.weekly_result = 0
            u.monthly_result = 0
            u.total_cash = 0
            u.total_given_cash = 0
            u.portfolio_value = 0
            u.save()
            u.topup_cash(config.STARTING_CASH)
