import asyncio

import pytest
from pytest_asyncio.plugin import event_loop_policy

# import uvloop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


pytest_plugins = [
    'tests.fixtures.auth.auth_service',
    'tests.fixtures.auth.clients',
    'tests.fixtures.users.user_repository',
    'tests.fixtures.infrastructure',
    'tests.fixtures.users.user_model'
]


@pytest.fixture(scope="function")
def event_loop(event_loop_policy):
    loop = event_loop_policy.new_event_loop()
    yield loop
    loop.close()

# @pytest.fixture(scope='session')
# def event_loop():
#     yield asyncio.get_event_loop()
#
# def pytest_sessionfinish(session, exitstatus):
#     asyncio.get_event_loop().close()
