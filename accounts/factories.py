import factory

from .models import UserProfile


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = 'johnsmith'
    name = 'John Smith'
