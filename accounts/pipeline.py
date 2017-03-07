# -*- coding: utf-8 -*-
import logging

# from django.conf import settings
# from django.contrib import messages
from django.core.files.base import ContentFile
# from django.core.mail import send_mail
from django.http.response import HttpResponseForbidden
# from django.utils.translation import ugettext as _

# from constance import config
from requests import request, HTTPError
from social.pipeline.partial import partial
# from twitter_api.models import User

from .models import UserProfile

logger = logging.getLogger(__name__)


@partial
def save_profile(strategy, user, response, details, is_new=False, *args, **kwargs):
    """
    Saves profile when logging with social auth.
    When new account then gets profile picture and checks number of
    friends/followers already in game. If more than
    config.REQUIRED_FRIENDS_THRESHOLD, then user is active by default.
    :type strategy: DjangoStrategy
    :param strategy: instance of strategy
    :type user: UserProfile
    :param user: instance of logging user
    :type response: dict
    :param response: response from social service
    :type details: dict
    :param details: details from social service (username, fullname, last_name, email, first_name)
    :type is_new: bool
    :param is_new: is it new account
    """
    #  uid = kwargs['uid']

    if not user or isinstance(user, HttpResponseForbidden):
        # user is unauthenticated
        return

    backend = kwargs['backend']

    if backend.name == 'twitter':
        if is_new or not user.is_active:
            # playing_followers_count = 0
            # tuser = User.remote.fetch(response.get('screen_name', ''))  # TODO: replace default value
            # followers = tuser.fetch_followers(all=True)
            # print(followers)
            # for follower in followers:
            #     try:
            #         follower_profile = UserProfile.objects.get('twitter_user_id', follower.id)
            #     except:
            #         pass
            #     else:
            #         if follower_profile.is_active:
            #             playing_followers_count += 1
            #
            # if playing_followers_count < config.REQUIRED_FRIENDS_THRESHOLD:
            #     user.is_active = False
            #     messages.warning(strategy.request,
            #                      _('Your account is inactive. Wait for administrator approval.'))
            #     if is_new:
            #         recipent_list = []
            #         for admin in UserProfile.objects.get_admins():
            #             if admin.email:
            #                 recipent_list.append(admin.email)
            #         if len(recipent_list) > 0:
            #             subject = u'Politikon - nowy użytkownik'
            #             message = u'Użytkownik czeka na akceptację. Aktywuj go pod ' + \
            #                 u'adresem: https://www.politikon.org.pl/admin/accounts/userprofile/'
            #             try:
            #                 from_email = settings.DEFAULT_EMAIL_FROM
            #                 send_mail(subject, message, from_email, recipent_list)
            #             except:
            #                 # TODO: handle error
            #                 logger.exception("Error: couldn't send emails")
            # else:
            user.is_active = True

            user.name = response.get('name', '')    # TODO: replace default value
            user.twitter_user_id = response['id']
            user.twitter_user = response.get('screen_name', '')  # TODO: replace default value
            user.save()

            if not response.get('default_profile_image'):
                url = response.get('profile_image_url', '').replace('_normal', '')
                try:
                    response = request('GET', url)
                    response.raise_for_status()
                except HTTPError:
                    pass
                else:
                    user.avatar.save('{0}_social.jpg'.format(user.username),
                                     ContentFile(response.content))

    if backend.name == 'facebook':
        if is_new or not user.is_active:
            # playing_friends_count = 0
            # print(response.get('friends', {}))
            # for friend in response.get('friends', {}).get('data', {}):
            #     try:
            #         friend_profile = UserProfile.objects.get('facebook_user_id', friend['id'])
            #     except:
            #         pass
            #     else:
            #         if friend_profile.is_active:
            #             playing_friends_count += 1
            #
            # if playing_friends_count < config.REQUIRED_FRIENDS_THRESHOLD:
            #     user.is_active = False
            #     messages.warning(strategy.request,
            #                      _('Your account is inactive. Wait for administrator approval.'))
            #     if is_new:
            #         recipent_list = []
            #         for admin in UserProfile.objects.get_admins():
            #             if admin.email:
            #                 recipent_list.append(admin.email)
            #         if len(recipent_list) > 0:
            #             subject = u'Politikon - nowy użytkownik'
            #             message = u'Użytkownik czeka na akceptację. Aktywuj go pod ' + \
            #                 u'adresem: https://www.politikon.org.pl/admin/accounts/userprofile/'
            #             try:
            #                 from_email = settings.DEFAULT_EMAIL_FROM
            #                 # TODO: fix it: https://trello.com/c/58h6fUgM/254-b-ad-wysy-ania-maili-na-heroku
            #                 send_mail(subject, message, from_email, recipent_list)
            #             except:
            #                 # TODO: handle error
            #                 logger.exception("Error: couldn't send emails")
            # else:
            user.is_active = True

            user.name = details['fullname']
            user.facebook_user = user.facebook_user_id = response['id']
            user.save()

            url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
            try:
                response = request('GET', url, params={'type': 'large'})
                response.raise_for_status()
            except HTTPError:
                pass
            else:
                user.avatar.save('{0}_social.jpg'.format(user.username),
                                 ContentFile(response.content))
