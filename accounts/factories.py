import factory

from .models import UserProfile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = factory.Sequence(lambda n: 'johnsmith%d' % n)
    name = factory.Sequence(lambda n: 'John Smith %d' % n)
    is_active = True


class UserWithAvatarFactory(UserFactory):
    username = factory.Sequence(lambda n: 'johnrambro%d' % n)
    name = factory.Sequence(lambda n: 'John Rambro %d' % n)
    avatar = factory.django.ImageField()


class AdminFactory(UserFactory):
    username = 'thomasshelby'
    name = 'Thomas Shelby'
    is_active = False
    is_staff = True
    is_admin = True
