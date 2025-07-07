import asyncio

import pytest


pytest_plugins = [
    'tests.fixtures.auth.auth_service',
    'tests.fixtures.auth.clients',
    'tests.fixtures.users.user_repository',
    'tests.fixtures.infrastructure',
    'tests.fixtures.users.user_model'
]


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    yield loop
    loop.close()
