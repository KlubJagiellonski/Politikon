from django.db import models


class EventManager(models.Manager):
    def ongoing_only_queryset(self):
        allowed_outcome = self.model.EVENT_OUTCOMES_DICT['IN_PROGRESS']
        return self.filter(outcome=allowed_outcome)

    def get_events(self, mode):
        if mode == 'popular':
            return self.ongoing_only_queryset().order_by('turnover')
        elif mode == 'latest':
            return self.ongoing_only_queryset().order_by('-created_date')
        elif mode == 'changed':
            return self.ongoing_only_queryset().order_by('-absolute_price_change')
        elif mode == 'finished':
            excluded_outcome = self.model.EVENT_OUTCOMES_DICT['IN_PROGRESS']
            return self.exclude(outcome=excluded_outcome).order_by('-end_date')

    def get_featured_events(self):
        return self.ongoing_only_queryset().filter(is_featured=True).order_by('estimated_end_date')

    def get_front_event(self):
        front_events = self.ongoing_only_queryset().filter(is_front=True).order_by('estimated_end_date')
        if front_events.count()>0:
            return front_events[0]
        else:
            return None

    def associate_people_with_events(self, user, events_list):
        event_ids = set([e.id for e in events_list])
        # friends = user.friends.all()
        bets = Bet.objects.select_related('user__facebook_user__profile_photo').filter(user__in=user.friends_ids_set, event__in=event_ids, has__gt=0)

        result = {
                    event_id: defaultdict(list)
                        # { outcome: defaultdict(list) for outcome in BET_OUTCOMES_DICT.keys() }
                            for event_id in event_ids
                 }

        for bet in bets:
            outcome = BET_OUTCOMES_INV_DICT[bet.outcome]
            result[bet.event_id][outcome].append(bet.user)

        return result


class BetManager(models.Manager):
    def get_users_bets_for_events(self, user, events):
        bets = self.filter(user__id=user.id, event__in=events)

        return bets

    def get_user_event_and_bet_for_update(self, user, event_id, for_outcome):
        event = list(Event.objects.select_for_update().filter(id=event_id))
        try:
            event = event[0]
        except IndexError:
            raise NonexistantEvent(_("Requested event does not exist."))

        if not event.is_in_progress:
            raise EventNotInProgress(_("Event is no longer in progress."))

        if for_outcome not in BET_OUTCOMES_DICT:
            raise UnknownOutcome()

        bet_outcome = BET_OUTCOMES_DICT[for_outcome]
        bet, created = self.get_or_create(user_id=user.id, event_id=event.id, outcome=bet_outcome)
        bet = list(self.select_for_update().filter(id=bet.id))[0]

        user = list(auth.get_user_model().objects.select_for_update().filter(id=user.id))[0]

        return user, event, bet

    def buy_a_bet(self, user, event_id, for_outcome, price):
        """ Always remember about wrapping this in a transaction! """
        user, event, bet = self.get_user_event_and_bet_for_update(user, event_id, for_outcome)

        if for_outcome == 'YES':
            transaction_type = self.model.TRANSACTION_TYPES_DICT['BUY_YES']
        else:
            transaction_type = self.model.TRANSACTION_TYPES_DICT['BUY_NO']

        requested_price = price
        current_tx_price = event.price_for_outcome(for_outcome, direction='BUY')
        if requested_price != current_tx_price:
            raise PriceMismatch(_("Price has changed."), event)

        quantity = 1
        bought_for_total = current_tx_price * quantity

        if (user.total_cash < bought_for_total):
            raise InsufficientCash(_("You don't have enough cash."), user)

        transaction = Transaction.objects.create(
                        user_id=user.id, event_id=event.id, type=transaction_type,
                        quantity=quantity, price=current_tx_price)

        event_total_bought_price = (bet.bought_avg_price * bet.bought)
        after_bought_quantity = bet.bought + quantity

        bet.bought_avg_price = (event_total_bought_price + bought_for_total) / after_bought_quantity
        bet.has += quantity
        bet.bought += quantity
        bet.save(update_fields=['bought_avg_price', 'has', 'bought'])

        user.total_cash -= bought_for_total
        user.save(update_fields=['total_cash'])

        event.increment_quantity(for_outcome, by_amount=quantity)
        """ Increment turnover only for buying bets """
        event.increment_turnover(quantity)
        event.save(force_update=True)

        # from canvas.models import ActivityLog
        # ActivityLog.objects.register_transaction_activity(user, transaction)

        PubNub().publish({
            'channel': event.publish_channel,
            'message': {
                'updates': {
                    'events': [event.event_dict]
                }
            }
        })

        return user, event, bet

    def sell_a_bet(self, user, event_id, for_outcome, price):
        """ Always remember about wrapping this in a transaction! """
        user, event, bet = self.get_user_event_and_bet_for_update(user, event_id, for_outcome)

        requested_price = price
        current_tx_price = event.price_for_outcome(for_outcome, direction='SELL')
        if requested_price != current_tx_price:
            raise PriceMismatch(_("Price has changed."), event)

        quantity = 1
        sold_for_total = current_tx_price * quantity

        if (bet.has < quantity):
            raise InsufficientBets(_("You don't have enough shares."), bet)

        if for_outcome == 'YES':
            transaction_type = self.model.TRANSACTION_TYPES_DICT['SELL_YES']
        else:
            transaction_type = self.model.TRANSACTION_TYPES_DICT['SELL_NO']

        transaction = Transaction.objects.create(
                        user_id=user.id, event_id=event.id, type=transaction_type,
                        quantity=quantity, price=current_tx_price)

        event_total_sold_price = (bet.sold_avg_price * bet.sold)
        after_sold_quantity = bet.sold + quantity

        bet.sold_avg_price = (event_total_sold_price + sold_for_total) / after_sold_quantity
        bet.has -= quantity
        bet.sold += quantity
        bet.save(update_fields=['sold_avg_price', 'has', 'sold'])

        user.total_cash += sold_for_total
        user.save(update_fields=['total_cash'])

        event.increment_quantity(for_outcome, by_amount=-quantity)
        event.save(force_update=True)

        # from canvas.models import ActivityLog
        # ActivityLog.objects.register_transaction_activity(user, transaction)

        PubNub().publish({
            'channel': event.publish_channel,
            'message': {
                'updates': {
                    'events': [event.event_dict]
                }
            }
        })

        return user, event, bet


class TransactionManager(models.Manager):
    pass

