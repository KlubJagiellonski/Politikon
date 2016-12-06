from datetime import timedelta

from django.contrib import auth
from django.db import models
from django.db.models import Q
from django.utils.timezone import now
from django.utils.translation import ugettext as _

from .exceptions import NonexistantEvent, PriceMismatch, EventNotInProgress, UnknownOutcome, \
    InsufficientCash, InsufficientBets
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
        allowed_outcome = self.model.EVENT_OUTCOME_CHOICES.IN_PROGRESS
        return self.filter(outcome=allowed_outcome)

    def get_events(self, mode):
        if mode == 'popular':
            return self.ongoing_only_queryset().order_by('-turnover')
        elif mode == 'last-minute':
            return self.ongoing_only_queryset().order_by('estimated_end_date')
        elif mode == 'latest':
            return self.ongoing_only_queryset().order_by('-created_date')
        elif mode == 'changed':
            return self.ongoing_only_queryset().order_by('-absolute_price_change')
        elif mode == 'finished':
            excluded_outcome = self.model.EVENT_OUTCOME_CHOICES.IN_PROGRESS
            return self.exclude(outcome=excluded_outcome).order_by('-end_date')

    def get_featured_events(self):
        excluded = self.get_events('last-minute').values('id')[:3]
        return self.ongoing_only_queryset().filter(is_featured=True).exclude(id__in=excluded)\
            .order_by('estimated_end_date')

    # TODO: what is this?
    #  def associate_people_with_events(self, user, events_list):
        #  from events.models import Bet

        #  event_ids = set([e.id for e in events_list])
        #  # friends = user.friends.all()
        #  bets = Bet.objects.select_related('user__facebook_user__profile_photo').\
            #  filter(user__in=user.friends_ids_set, event__in=event_ids, has__gt=0)

        #  result = {
            #  event_id: defaultdict(list)
            #  # { outcome: defaultdict(list) for
            #  # outcome in BET_OUTCOMES_DICT.keys() }
            #  for event_id in event_ids
        #  }

        #  for bet in bets:
            #  outcome = BET_OUTCOMES_INV_DICT[bet.outcome]
            #  result[bet.event_id][outcome].append(bet.user)

        #  return result

    def vote_for_solution(self, user, event_id, outcome):
        """
        User votes for a solution of an event.
         1. Increment decision of event value,
         2. Create object to remember user's decision,
         3. Return values of both couns
        :type user: request user
        :param user: voting user
        :type event_id: int
        :param event_id: event id
        :type outcome: string
        :param outcome: YES or NO
        :return:
        """
        try:
            event = self.model.objects.get(id=event_id)
        except:
            raise NonexistantEvent(_("Requested event does not exist."))

        if not event.is_in_progress:
            raise EventNotInProgress(_("Event is no longer in progress."))

        from .models import SolutionVote
        vote, created = SolutionVote.objects.get_or_create(user_id=user.id, event_id=event.id)
        if outcome == 'YES':
            outcome_vote = SolutionVote.VOTE_OUTCOME_CHOICES.YES
        elif outcome == 'NO':
            outcome_vote = SolutionVote.VOTE_OUTCOME_CHOICES.NO
        elif outcome == 'CANCEL':
            outcome_vote = SolutionVote.VOTE_OUTCOME_CHOICES.CANCEL
        else:
            raise UnknownOutcome(_("Unknown outcome."))

        if created or vote.outcome != outcome_vote:
            if vote.outcome != outcome_vote:
                if vote.outcome == SolutionVote.VOTE_OUTCOME_CHOICES.YES:
                    event.vote_yes_count -= 1
                elif vote.outcome == SolutionVote.VOTE_OUTCOME_CHOICES.NO:
                    event.vote_no_count -= 1
                elif vote.outcome == SolutionVote.VOTE_OUTCOME_CHOICES.CANCEL:
                    event.vote_cancel_count -= 1
                event.save()
            vote.outcome = outcome_vote
            if outcome == 'YES':
                event.vote_yes()
            elif outcome == 'NO':
                event.vote_no()
            elif outcome == 'CANCEL':
                event.vote_cancel()
            vote.save()
        return {
            'YES': event.vote_yes_count,
            'NO': event.vote_no_count,
            'CANCEL': event.vote_cancel_count
        }


class BetManager(models.Manager):
    def get_user_bets_for_events(self, user, events):
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
        bet, created = self.get_or_create(user_id=user.id, event_id=event.id, outcome=bet_outcome)
        bet = list(self.select_for_update().filter(id=bet.id))[0]

        user = list(auth.get_user_model().objects.select_for_update().filter(id=user.id))[0]

        return user, event, bet

    def buy_a_bet(self, user, event_id, for_outcome, price):
        """ Always remember about wrapping this in a transaction! """

        from events.models import Transaction

        user, event, bet = self.get_user_event_and_bet_for_update(user, event_id, for_outcome)

        if for_outcome == 'YES':
            transaction_type = Transaction.TRANSACTION_TYPE_CHOICES.BUY_YES
        else:
            transaction_type = Transaction.TRANSACTION_TYPE_CHOICES.BUY_NO

        requested_price = price
        current_tx_price = event.price_for_outcome(for_outcome, direction='BUY')
        if requested_price != current_tx_price:
            raise PriceMismatch(_("Price has changed."), event)

        quantity = 1
        bought_for_total = current_tx_price * quantity

        if user.total_cash < bought_for_total:
            raise InsufficientCash(_("You don't have enough cash."), user)

        Transaction.objects.create(
            user_id=user.id,
            event_id=event.id,
            type=transaction_type,
            quantity=quantity,
            price=current_tx_price * -1
        )

        event_total_bought_price = (bet.bought_avg_price * bet.bought)
        after_bought_quantity = bet.bought + quantity

        bet.bought_avg_price = (event_total_bought_price +
                                bought_for_total) / after_bought_quantity
        bet.has += quantity
        bet.bought += quantity
        bet.save(update_fields=['bought_avg_price', 'has', 'bought'])

        user.total_cash -= bought_for_total
        user.portfolio_value += bought_for_total
        user.save()

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
            transaction_type = Transaction.TRANSACTION_TYPE_CHOICES.SELL_YES
        else:
            transaction_type = Transaction.TRANSACTION_TYPE_CHOICES.SELL_NO

        Transaction.objects.create(
            user_id=user.id,
            event_id=event.id,
            type=transaction_type,
            quantity=quantity,
            price=current_tx_price
        )

        event_total_sold_price = (bet.sold_avg_price * bet.sold)
        after_sold_quantity = bet.sold + quantity

        bet.sold_avg_price = (event_total_sold_price + sold_for_total) / after_sold_quantity
        bet.has -= quantity
        bet.sold += quantity
        bet.save(update_fields=['sold_avg_price', 'has', 'sold'])

        user.total_cash += sold_for_total
        user.portfolio_value -= sold_for_total
        user.save()

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
        ).order_by('event__estimated_end_date')

    def get_finished(self, user):
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
            user=user
        ).filter(Q(event__end_date__isnull=True) | Q(event__end_date__gte=user.reset_date)).\
            order_by('-event__end_date')


class TransactionManager(models.Manager):
    """
    Transactions Manager between user and event
    """
    def __init__(self):
        """
        set model as Transaction model
        """
        super(TransactionManager, self).__init__()

    def get_user_transactions_after_reset(self, user):
        return self.model.objects.filter(user=user, date__gte=user.reset_date).order_by('-date')

    def get_cumulated_user_transactions(self, user):
        queryset = self.get_user_transactions_after_reset(user)
        old = None
        result = []
        for q in queryset:
            if old is None:
                old = q
            elif q.type == old.type and q.event == old.event:
                old.price += q.price
            else:
                result.append(old)
                old = q
        if len(result) == 0 or q != result[-1]:
            result.append(q)
        return result

    def get_user_transactions(self, user):
        return self.model.objects.filter(user=user).\
            exclude(type=self.model.TRANSACTION_TYPE_CHOICES.TOPPED_UP_BY_APP)

    def get_weekly_user_transactions(self, user):
        last_week = now() - timedelta(days=7)
        return self.get_user_transactions(user).filter(date__gt=last_week)

    def get_monthly_user_transactions(self, user):
        last_month = now() - timedelta(days=30)
        return self.get_user_transactions(user).filter(date__gt=last_month)

    def get_queryset(self):
        """
        Get transactions younger than reset_date. It is for respecting "account reset"
        :return: QuerySet active transactions
        :rtype: QuerySet[Transactions]
        """
        queryset = super(TransactionManager, self).get_queryset()
        return queryset.filter(date__gte=models.F('user__reset_date'))
