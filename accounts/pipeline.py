import logging

from django.core.files.base import ContentFile
from social.pipeline.partial import partial

from constance import config
from requests import request, HTTPError

from .models import UserProfile

logger = logging.getLogger(__name__)


@partial
def save_profile(strategy, user, response, details,
                 is_new=False, *args, **kwargs):
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
    :param details: details from social service (username, fullname, last_name,
    email, first_name)
    :type is_new: bool
    :param is_new: is it new account
    """
    # print(is_new)
    # print(response)
    # print(strategy)
    # print(details)
    # uid = kwargs['uid']

    backend = kwargs['backend']

    if is_new and backend.name == 'twitter':
        user.name = response['name']
        user.twitter_user_id = response['id']
        user.twitter_user = response['screen_name']
        user.save()

        if not response['default_profile_image']:
            url = response['profile_image_url'].replace('_normal', '')
            try:
                response = request('GET', url)
                response.raise_for_status()
            except HTTPError:
                pass
            else:
                user.avatar.save('{0}_social.jpg'.format(user.username),
                                 ContentFile(response.content))

    if is_new and backend.name == 'facebook':
        playing_friends_count = 0
        for friend in response['friends']['data']:
            try:
                user = UserProfile.objects.\
                    get('facebook_user_id', friend['id'])
            except:
                pass
            else:
                if user.is_active:
                    playing_friends_count += 1

        if playing_friends_count < config.REQUIRED_FRIENDS_THRESHOLD:
            user.is_active = False
        else:
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
