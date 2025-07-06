from dataclasses import dataclass
import pytest
import httpx
from faker import Factory

from app.settings import settings
from app.users.auth.schema import GoogleUserData, YandexUserData
from tests.fixtures.users.user_model import TEST_GOOGLE_USER_ID, TEST_GOOGLE_USER_EMAIL

faker = Factory.create()


@dataclass
class FakeGoogleClient:
    settings: settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token(code=code)
        return google_user_info_data()

    async def _get_user_access_token(self, code: str) -> str:
        return (f'fake access token {code}')


@dataclass
class FakeYandexClient:
    settings: settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> YandexUserData:
        access_token = await self._get_user_access_token(code=code)
        return yandex_user_info_data()

    async def _get_user_access_token(self, code: str) -> str:
        return (f'fake access token {code}')


@pytest.fixture
def google_client(settings):
    return FakeGoogleClient(settings=settings, async_client=httpx.AsyncClient())


@pytest.fixture
def yandex_client(settings):
    return FakeYandexClient(settings=settings, async_client=httpx.AsyncClient())


def google_user_info_data() -> GoogleUserData:
    return GoogleUserData(
        id=TEST_GOOGLE_USER_ID,
        email=TEST_GOOGLE_USER_EMAIL,
        name=faker.name(),
        access_token=faker.sha256(),
        verified_email=True
    )


def yandex_user_info_data() -> YandexUserData:
    return YandexUserData(
        id=faker.random_int(),
        default_email=faker.email(),
        login=faker.name(),
        access_token=faker.sha256(),
        real_name=faker.name()
    )
