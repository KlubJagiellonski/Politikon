import factory

from .models import UserProfile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = factory.Sequence(lambda n: 'johnsmith%d' % n)
    name = factory.Sequence(lambda n: 'John Smith %d' % n)
    is_active = True


class UserWithAvatarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = factory.Sequence(lambda n: 'johnrambro%d' % n)
    name = factory.Sequence(lambda n: 'John Rambro %d' % n)
    is_active = True
    avatar = factory.django.ImageField()


class AdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = 'thomasshelby'
    name = 'Thomas Shelby'
    is_staff = True
    is_admin = True
