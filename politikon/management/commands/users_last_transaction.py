from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from events.models import Transaction, Bet, Event
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Updates users last transaction date'

    def handle(self, *args, **options):
        for user in UserProfile.objects.all():
            transactions = Transaction.objects.filter(user=user, type__in=Transaction.BUY_SELL_TYPES).\
                order_by('-date')[:1]
            if len(transactions):
                user.last_transaction = transactions[0].date
                user.save()
