from collections import defaultdict
from dateutil.relativedelta import relativedelta

from django.contrib import auth
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext as _

from .exceptions import NonexistantEvent, PriceMismatch, EventNotInProgress, \
    UnknownOutcome, InsufficientCash, InsufficientBets
# from vendor.Pubnub import Pubnub as PubNub


BET_OUTCOMES_DICT = {
    'YES': True,
    'NO': False,
}

BET_OUTCOMES_INV_DICT = {
    True: 'YES',
    False: 'NO',
}


class EventManager(models.Manager):
    def ongoing_only_queryset(self):
        from events.models import Event
        allowed_outcome = Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS
        return self.filter(outcome=allowed_outcome)

    def get_events(self, mode):
        from events.models import Event
        if mode == 'popular':
            return self.ongoing_only_queryset().order_by('turnover')
        elif mode == 'latest':
            return self.ongoing_only_queryset().order_by('-created_date')
        elif mode == 'changed':
            return self.ongoing_only_queryset().\
                order_by('-absolute_price_change')
        elif mode == 'finished':
            excluded_outcome = Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS
            return self.exclude(outcome=excluded_outcome).order_by('-end_date')

    def get_in_progress(self):
        from events.models import Event
        return self.filter(outcome=Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS)


    def get_featured_events(self):
        return self.ongoing_only_queryset().filter(is_featured=True).\
            order_by('estimated_end_date')

    def get_front_event(self):
        front_events = self.ongoing_only_queryset().filter(is_front=True)\
            .order_by('estimated_end_date')
        if front_events.exists():
            return front_events[0]
        else:
            return None

    def associate_people_with_events(self, user, events_list):
        from events.models import Bet

        event_ids = set([e.id for e in events_list])
        # friends = user.friends.all()
        bets = Bet.objects.\
            select_related('user__facebook_user__profile_photo').\
            filter(user__in=user.friends_ids_set,
                   event__in=event_ids, has__gt=0)

        result = {
            event_id: defaultdict(list)
            # { outcome: defaultdict(list) for
            # outcome in BET_OUTCOMES_DICT.keys() }
            for event_id in event_ids
        }

        for bet in bets:
            outcome = BET_OUTCOMES_INV_DICT[bet.outcome]
            result[bet.event_id][outcome].append(bet.user)

        return result


class BetManager(models.Manager):
    def get_users_bets_for_events(self, user, events):
        return self.filter(user__id=user.id, event__in=events)

    def get_user_event_and_bet_for_update(self, user, event_id, for_outcome):
        from events.models import Event
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
        bet, created = self.get_or_create(user_id=user.id, event_id=event.id,
                                          outcome=bet_outcome)
        bet = list(self.select_for_update().filter(id=bet.id))[0]

        user = list(auth.get_user_model().objects.
                    select_for_update().filter(id=user.id))[0]

        return user, event, bet

    def buy_a_bet(self, user, event_id, for_outcome, price):
        """ Always remember about wrapping this in a transaction! """

        from events.models import Transaction

        user, event, bet = self.get_user_event_and_bet_for_update(user,
                                                                  event_id,
                                                                  for_outcome)

        if for_outcome == 'YES':
            transaction_type = Transaction.TRANSACTION_TYPE_CHOICES.BUY_YES
        else:
            transaction_type = Transaction.TRANSACTION_TYPE_CHOICES.BUY_NO

        requested_price = price
        current_tx_price = event.price_for_outcome(for_outcome,
                                                   direction='BUY')
        if requested_price != current_tx_price:
            raise PriceMismatch(_("Price has changed."), event)

        quantity = 1
        bought_for_total = current_tx_price * quantity

        if (user.total_cash < bought_for_total):
            raise InsufficientCash(_("You don't have enough cash."), user)

        Transaction.objects.create(
            user_id=user.id, event_id=event.id, type=transaction_type,
            quantity=quantity, price=current_tx_price)

        event_total_bought_price = (bet.bought_avg_price * bet.bought)
        after_bought_quantity = bet.bought + quantity

        bet.bought_avg_price = (event_total_bought_price +
                                bought_for_total) / after_bought_quantity
        bet.has += quantity
        bet.bought += quantity
        bet.save(update_fields=['bought_avg_price', 'has', 'bought'])

        user.total_cash -= bought_for_total
        user.portfolio_value += bought_for_total
        user.save(update_fields=['total_cash', 'portfolio_value'])
        user.calculate_reputation()
        user.save(update_fields=['reputation'])

        event.increment_quantity(for_outcome, by_amount=quantity)
        """ Increment turnover only for buying bets """
        event.increment_turnover(quantity)
        event.save(force_update=True)

        # from canvas.models import ActivityLog
        # ActivityLog.objects.register_transaction_activity(user, transaction)

        # # TODO: To z jakiegos powodu nie dziala
        # PubNub().publish({
        #     'channel': event.publish_channel,
        #     'message': {
        #         'updates': {
        #             'events': [event.event_dict]
        #         }
        #     }
        # })

        return user, event, bet

    def sell_a_bet(self, user, event_id, for_outcome, price):
        """ Always remember about wrapping this in a transaction! """
        from events.models import Transaction

        user, event, bet = self.get_user_event_and_bet_for_update(user,
                                                                  event_id,
                                                                  for_outcome)

        requested_price = price
        current_tx_price = event.price_for_outcome(for_outcome,
                                                   direction='SELL')
        if requested_price != current_tx_price:
            raise PriceMismatch(_("Price has changed."), event)

        quantity = 1
        sold_for_total = current_tx_price * quantity

        if (bet.has < quantity):
            raise InsufficientBets(_("You don't have enough shares."), bet)

        if for_outcome == 'YES':
            transaction_type = Transaction.TRANSACTION_TYPE_CHOICES.SELL_YES
        else:
            transaction_type = Transaction.TRANSACTION_TYPE_CHOICES.SELL_NO

        Transaction.objects.create(
            user_id=user.id, event_id=event.id, type=transaction_type,
            quantity=quantity, price=current_tx_price)

        event_total_sold_price = (bet.sold_avg_price * bet.sold)
        after_sold_quantity = bet.sold + quantity

        bet.sold_avg_price = (event_total_sold_price +
                              sold_for_total) / after_sold_quantity
        bet.has -= quantity
        bet.sold += quantity
        bet.save(update_fields=['sold_avg_price', 'has', 'sold'])

        user.total_cash += sold_for_total
        user.portfolio_value -= sold_for_total
        user.save(update_fields=['total_cash', 'portfolio_value'])
        user.calculate_reputation()
        user.save(update_fields=['reputation'])

        event.increment_quantity(for_outcome, by_amount=-quantity)
        event.increment_turnover(quantity)
        event.save(force_update=True)

        # from canvas.models import ActivityLog
        # ActivityLog.objects.register_transaction_activity(user, transaction)

        # # TODO: To z jakiegos powodu nie dziala
        # PubNub().publish({
        #     'channel': event.publish_channel,
        #     'message': {
        #         'updates': {
        #             'events': [event.event_dict]
        #         }
        #     }
        # })

        return user, event, bet

    def get_in_progress(self):
        """
        Get bets in progress and attribute has > 0, that bets are in user
        wallet.
        :return: Bets in user wallet
        :rtype: QuerySet[Bet]
        """
        from events.models import Event
        return self.filter(
            event__outcome=Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS,
            has__gt=0,
        )

    def get_finished(self):
        """
        Get finished bets and attribute has > 0, that bets are on user result
        list.
        :return: Bets on user result list
        :rtype: QuerySet[Bet]
        """
        from events.models import Event
        events_finshed = (
            Event.EVENT_OUTCOME_CHOICES.CANCELLED,
            Event.EVENT_OUTCOME_CHOICES.FINISHED_YES,
            Event.EVENT_OUTCOME_CHOICES.FINISHED_NO,
        )
        return self.filter(
            event__outcome__in=events_finshed,
            has__gt=0,
        )


class TransactionManager(models.Manager):
    def get_user_transactions(self, user):
        from events.models import Transaction
        return self.get_queryset().filter(user=user).\
            exclude(type=Transaction.TRANSACTION_TYPE_CHOICES.TOPPED_UP_BY_APP)

    def get_weekly_user_transactions(self, user):
        last_week = now() - relativedelta(weeks=1)
        return self.get_user_transactions(user).filter(date__gt=last_week)

    def get_monthly_user_transactions(self, user):
        last_month = now() - relativedelta(months=1)
        return self.get_user_transactions(user).filter(date__gt=last_month)
