from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from events.models import Transaction, Bet, Event
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Resets all accounts and ongoing events results'

    def add_arguments(self, parser):
        parser.add_argument(
            '--bonus',
            default=0,
            dest='bonus',
            type=float
        )

    def handle(self, *args, **options):

        for t in Transaction.objects.filter(type=Transaction.TRANSACTION_TYPE_CHOICES.TOPPED_UP_BY_APP):
            t.delete()

        for t in Transaction.objects.filter(event__outcome=Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS):
            t.delete()

        for b in Bet.objects.filter(event__outcome=Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS):
            b.delete()

        for e in Event.objects.ongoing_only_queryset():
            e.quantity = 0
            e.Q_against = e.Q_for = 0
            e.recalculate_prices()
            e.save()

        for u in UserProfile.objects.get_users():
            u.reset_account(Decimal(options['bonus']))
            u.save()
