import factory

from .models import UserProfile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = 'johnsmith'
    name = 'John Smith'


class BaBroracusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = 'babroracus'
    name = 'Ba Broracus'


class BroHardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = 'brohard'
    name = 'Bro Hard'


class AdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = 'thomasshelby'
    name = 'Thomas Shelby'
    is_staff = True
    is_admin = True
