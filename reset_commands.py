from datetime import timedelta
from events.models import Transaction, Bet, Event
from accounts.models import UserProfile
from constance import config
from django.utils.timezone import now


for t in Transaction.objects.filter(event__is_in_progress=True):
    t.delete()
for b in Bet.objects.filter(event__is_in_progress=True):
    b.delete()
for e in Event.objects.ongoing_only_queryset():
    e.recalculate_prices()
for u in UserProfile.objects.get_users():
    u.active_date = now() - timedelta(years=1)
    u.save()
    u.topup_cash(config.STARTING_CASH)
