import pytest_asyncio

from app.dependency import get_broker_producer
from app.settings import settings as conf
from app.users.auth.clients import MailClient
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository


@pytest_asyncio.fixture
async def mock_auth_service(yandex_client ,google_client, fake_user_repository, mail_client):
    return AuthService(
        user_repository=fake_user_repository,
        settings=conf,
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=mail_client
    )


@pytest_asyncio.fixture
async def auth_service(yandex_client, google_client, mock_auth_service, db_session):
    return AuthService(
        user_repository=UserRepository(db_session=db_session),
        google_client=google_client,
        yandex_client=yandex_client,
        settings=conf,
        mail_client=MailClient(settings=conf, broker_producer=await get_broker_producer())
    )
