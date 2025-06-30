import pytest

from app.settings import settings as s


@pytest.fixture
def settings():
    return s
