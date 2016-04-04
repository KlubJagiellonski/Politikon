import factory

from .models import UserProfile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = 'johnsmith'
    name = 'John Smith'


class AdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = 'thomasshelby'
    name = 'Thomas Shelby'
    is_staff = True
    is_admin = True
    is_active = True
