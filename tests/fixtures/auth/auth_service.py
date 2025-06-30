import pytest

from app.settings import settings as conf
from app.users.auth.service import AuthService


@pytest.fixture
def auth_service(yandex_client ,google_client, fake_user_repository):
    return AuthService(
        user_repository=fake_user_repository,
        settings=conf,
        google_client=google_client,
        yandex_client=yandex_client
    )
