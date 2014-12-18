from django.contrib import auth
from django.contrib.auth import authenticate, login

import logging
logger = logging.getLogger(__name__)

#TODO: remove the whole file after proper auth is done

class DummyCookieMiddleware( object ):
    def process_request(self, request):
        if "user_id" not in request.COOKIES:
            return

        id = request.COOKIES["user_id"]

        user = authenticate(user_id=id)

        request.user = user
        login(request, user)

class DummyCookieAuth:
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, user_id):
        return self.get_user(user_id)

    def get_user(self, user_id):
        user_model_class = auth.get_user_model()

        try:
            return user_model_class.objects.get(pk=user_id)
        except user_model_class.DoesNotExist:
            return None
