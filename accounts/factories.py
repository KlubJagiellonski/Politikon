import factory

from .models import UserProfile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = 'johnsmith'
    name = 'John Smith'
    is_active = True


class BaBroracusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = 'babroracus'
    name = 'Ba Broracus'
    is_active = True


class BroHardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = 'brohard'
    name = 'Bro Hard'
    is_active = True


class AdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = 'thomasshelby'
    name = 'Thomas Shelby'
    is_staff = True
    is_admin = True
