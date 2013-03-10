# coding: utf-8
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import F, Q
from django.utils.translation import ugettext as _

from constance import config
from canvas.models import FacebookUser

import datetime

class UserManager(BaseUserManager):
    def return_new_user_object(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username address')

        user = self.model(
            username=UserManager.normalize_email(username),
        )

        user.set_password(password)

        return user

    def create_user(self, username, password=None):
        user = self.return_new_user_object(username)
        user.is_active = True

        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.return_new_user_object(username,
            password=password,
        )
        user.is_admin = True
        user.is_active = True

        user.save(using=self._db)
        return user

    def create_user_with_random_password(self, username, **kwargs):
        user = self.return_new_user_object(username,
            password=None
        )
        password = self.make_random_password()
        user.set_password(password)

        for keyword, argument in kwargs.items():
            setattr(user, keyword, argument)

        user.save(using=self._db)
        return user, password

    def get_for_facebook_user(self, facebook_user):
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
            user.rebuild_facebook_friends()
            user.save()

        return user


class User(AbstractBaseUser):
    objects = UserManager()

    username = models.CharField(u"email", max_length=1024, unique=True)
    name = models.CharField(max_length=1024, blank=True)
    is_active = models.BooleanField(u"can log in", default=True)
    is_admin = models.BooleanField(u"is an administrator", default=False)
    is_deleted = models.BooleanField(u"is deleted", default=False)

    created_date = models.DateTimeField(auto_now_add=True)

#   Every new network relations also has to have 'related_name="django_user"'
    facebook_user = models.OneToOneField(FacebookUser, null=True, related_name="django_user")

    friends = models.ManyToManyField('self', related_name='friend_of')

    total_cash = models.FloatField(u"ilość gotówki", default=0.)
    total_given_cash = models.FloatField(u"ilość przyznanej gotówki w historii", default=0.)

    USERNAME_FIELD = 'username'

    def rebuild_facebook_friends(self):
        # Delete current relations.
        relations_Q = Q(from_user=self) | Q(to_user=self)

        friends_manager = self.friends.through.objects
        friends_manager.filter(relations_Q).delete()

        # Recreate friends
        facebook_friends_ids = self.facebook_user.friends_using_our_app
        fresh_friends = FacebookUser.objects.django_users_for_ids(facebook_friends_ids)

        self.friends.add(fresh_friends)

    @property
    def statistics_dict(self):
        return {
            'user_id': self.id,
            'total_cash': "%.2f" % self.total_cash,
        }

    def get_full_name(self):
        return "%s (%s)" % (self.name, self.username)

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
            return True

    def has_module_perms(self, app_label):
        return True

    def topup_cash(self, amount):
        self.total_cash = F('total_cash') + amount
        self.total_given_cash = F('total_given_cash') + amount

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

