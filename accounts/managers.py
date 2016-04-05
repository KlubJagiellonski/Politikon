# -*- coding: utf-8 -*-
from django.contrib.auth.models import BaseUserManager
from django.http import HttpResponseForbidden

from .utils import process_username
from constance import config


class UserProfileManager(BaseUserManager):
    def return_new_user_object(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username address')

        user = self.model(
            username=UserProfileManager.normalize_email(username),
        )

        user.set_password(password)

        return user

    def create_user(self, username, email, password=None):
        if len(self.model.objects.filter(email=email)) > 0 and len(email) > 0:
            return HttpResponseForbidden()
        username = process_username(username)
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        user.topup_cash(config.STARTING_CASH)

        return user

    def create_superuser(self, username, email, password=None):
        if len(self.model.objects.filter(email=email)) > 0 and len(email) > 0:
            return HttpResponseForbidden()
        username = process_username(username)
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)

        return user

    def create_user_with_random_password(self, username, **kwargs):
        username = process_username(username)
        user = self.return_new_user_object(
            username,
            password=None
        )
        password = self.make_random_password()
        user.set_password(password)

        for keyword, argument in kwargs.items():
            setattr(user, keyword, argument)

        user.save(using=self._db)
        return user, password

    def get_for_facebook_user(self, facebook_user):
        try:
            return facebook_user.django_user
        except self.model.DoesNotExist:
            pass

        user, created = self.get_or_create(username=facebook_user.facebook_id)
        user_has_changed = False

        if user.facebook_user_id != facebook_user.id:
            user.facebook_user = facebook_user
            user_has_changed = True
        if created:
            user.total_cash = config.STARTING_CASH
            user.total_given_cash = config.STARTING_CASH
            user_has_changed = True

        if user_has_changed:
            user.synchronize_facebook_friends()
            user.save()

        # if created:
        # from canvas.models import ActivityLog
        #     ActivityLog.objects.register_new_user_activity(user)

        # logger.debug("UserManager(user %s).get_for_facebook_user(%s), \
            # created: %d, has_chaged: %d" % (
            # unicode(user), unicode(facebook_user),
            # created, user_has_changed))

        return user

    def get_users(self):
        return self.get_queryset().filter(is_active=True, is_deleted=False)

    def get_admins(self):
        return self.get_queryset().filter(is_staff=True, is_admin=True)

    def get_best_weekly(self):
        return self.get_users().filter(weekly_result__isnull=False).\
            order_by('-weekly_result')

    def get_best_monthly(self):
        return self.get_users().filter(monthly_result__isnull=False).\
            order_by('-monthly_result')

    def get_best_overall(self):
        """
        Get users ordered by the best reputation
        :return: UserProfiles list
        :rtype: QuerySet
        """
        return self.get_users().order_by('-reputation')

    def get_user_positions(self, user):
        best_weekly = list(self.get_best_weekly())
        best_monthly = list(self.get_best_monthly())
        best_overall = list(self.get_best_overall())
        week_rank = "-"
        month_rank = "-"
        overall_rank = "-"
        if user in best_weekly:
            week_rank = best_weekly.index(user) + 1
        if user in best_monthly:
            month_rank = best_monthly.index(user) + 1
        if user in best_overall:
            overall_rank = best_overall.index(user) + 1
        return {
            'week_rank': week_rank,
            'month_rank': month_rank,
            'overall_rank': overall_rank
        }
