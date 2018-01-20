# -*- coding: utf-8 -*-
import uuid
from unidecode import unidecode

from django.utils.crypto import get_random_string


def process_username(username):
    username = unidecode(username)
    # TODO self.name = username for casual users
    # and username = email b/c username has to be unique
    from .models import UserProfile
    while len(UserProfile.objects.filter(username=username)) > 0:
        username = uuid.uuid4().hex[:30]

    return username


def generate_random_string(length=30):
    return get_random_string(length)

