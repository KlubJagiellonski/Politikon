from .models import Bet


def create_bets_dict(user, events):
    # TODO: remove it
    # DEPRECATED use event.get_user_bet(user)
    bets = dict()
    if user is not None:
        bets = Bet.objects.get_users_bets_for_events(user, events)
        bets = dict((bet.event_id, bet) for bet in bets)

    all_bets = dict()
    if len(events) > 1 and len(bets) > 0:
        for event in events:
            if event.id in bets and bets[event.id].has > 0:
                bet = bets[event.id]
                all_bets[event.id] = {
                    'has_any': True,
                    'buyYES': bet.outcome,
                    'buyNO': not bet.outcome,
                    'outcomeYES': "YES" if bet.outcome else "NO",
                    'outcomeNO': "YES" if bet.outcome else "NO",
                    'priceYES': event.current_buy_for_price if bet.outcome
                    else event.current_sell_against_price,
                    'priceNO': event.current_sell_for_price if bet.outcome
                    else event.current_buy_against_price,
                    'textYES': "+" if bet.outcome else "-",
                    'textNO': "-" if bet.outcome else "+",
                    'has': bet.has,
                    'classOutcome': "YES" if bet.outcome else "NO",
                    'textOutcome': "TAK" if bet.outcome else "NIE",
                    'avgPrice': round(bet.bought_avg_price, 2),
                }
            else:
                all_bets[event.id] = {
                    'has_any': False,
                    'buyYES': True,
                    'buyNO': True,
                    'outcomeYES': "YES",
                    'outcomeNO': "NO",
                    'priceYES': event.current_buy_for_price,
                    'priceNO': event.current_buy_against_price,
                    'textYES': "TAK",
                    'textNO': "NIE"
                }

    return all_bets
