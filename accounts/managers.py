from django.contrib.auth.models import BaseUserManager, UserManager


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
        user = self.model(
            username = username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
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

        logger.debug("UserManager(user %s).get_for_facebook_user(%s), created: %d, has_chaged: %d" % (
            unicode(user), unicode(facebook_user), created, user_has_changed))

        return user
