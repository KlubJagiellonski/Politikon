from django.contrib import auth


class FacebookCanvasFandjangoBackend:
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, fandjango_user=None):
        user_model_class = auth.get_user_model()

        if not fandjango_user:
            return None

        django_user = user_model_class.objects.get_for_facebook_user(fandjango_user)

        return django_user

    def get_user(self, user_id):
        user_model_class = auth.get_user_model()

        try:
            return user_model_class.objects.get(pk=user_id)
        except user_model_class.DoesNotExist:
            return None
