import factory
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from app.users.user_profile.models import UserProfile

faker = FakerFactory.create()


TEST_GOOGLE_USER_ID = 20
TEST_GOOGLE_USER_EMAIL = 'google.test@test.mail'


@register(_name='user_profile')
class UserProfileFactory(factory.Factory):
    class Meta:
        model = UserProfile

    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.name())
    email = factory.LazyFunction(lambda: faker.email())
    name = factory.LazyFunction(lambda: faker.name())

