from accounts.models import UserProfile
from events.models import Event, Bet, Transaction
from django.utils.timezone import now

us = UserProfile.objects.all()
for u in us:
    u.active_date = now()
    u.total_cash = u.portfolio_value = 0
    u.weekly_result = u.monthly_result = None
    u.reputation = 100
    u.total_given_cash = 1000
    u.save()

for b in Bet.objects.all():
    b.has = b.bought = b.sold = b.bought_avg_price = b.sold_avg_price = b.rewarded_total = 0

for e in Event.objects.all():
    e.current_buy_for_price = e.current_buy_against_price = e.current_sell_for_price = e.current_sell_against_price = 50
    e.Q_for = e.Q_against = 0
    e.turnover = 0
    e.absolute_price_change = 0
    e.price_change = 0
    e.save()

# reset snapshots

# execute: accounts.tasks, events.tasks

