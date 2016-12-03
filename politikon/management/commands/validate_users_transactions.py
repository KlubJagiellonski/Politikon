from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from events.models import Transaction, Bet, Event
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Validates user\'s transactions'

    def handle(self, *args, **options):

        below_zero = []
        users_below_zero = set()
        for user in UserProfile.objects.all():
            user_money = 0

            # trace debit transactions and erase 'em
            for transaction in Transaction.objects.filter(user=user, date__gte=user.reset_date).order_by('date'):
                if user_money + (transaction.price * transaction.quantity) < 0:
                    # rollback stock price
                    # TODO
                    # erase transaction
                    below_zero.append((user, transaction, user_money))
                    print('{0} {1} {2}'.format(user, transaction.date, user_money))
                    users_below_zero.add(user)
                    transaction.delete()
                else:
                    user_money += transaction.price * transaction.quantity

            # trace selling nonexistent bets, erase 'em and update user's bets
            bets = {}
            for transaction in Transaction.objects.filter(user=user, date__gte=user.reset_date).order_by('date'):
                if transaction.type in transaction.BUY_SELL_TYPES:
                    if transaction.event in bets:
                        bets[transaction.event]
                    else:
                        if transaction.type in transaction.BUY_TYPES:
                            bets[transaction.event] = {
                                'outcome': transaction.outcome,
                                'quantity': transaction.quantity,
                            }

            # trace solve event mismatch
            # recalculate reputation and wallet value
            # recalculate prices

        print(len(below_zero))
        print(len(users_below_zero))
        print(users_below_zero)
