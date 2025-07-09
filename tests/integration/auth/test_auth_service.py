import pytest
from sqlalchemy import select, insert

from app.users.user_profile.models import UserProfile
from tests.fixtures.users.user_model import TEST_GOOGLE_USER_ID, TEST_GOOGLE_USER_EMAIL

pytestmark = pytest.mark.asyncio


async def test_google_auth__login_not_exist_user(auth_service, db_session):
    code = 'fake_code'

    async with db_session as session:
        users = (await session.execute(select(UserProfile))).scalars().all()
        session.expire_all()

    user = await auth_service.google_auth(code)

    assert len(users) == 0
    assert user is not None

    async with db_session as session:
        login_user = (await session.execute(select(UserProfile).where(UserProfile.id == user.user_id))).scalars().first()
        session.expire_all()

    assert login_user is not None


async def test_google_auth__login_exist_user(auth_service, db_session):
    query = insert(UserProfile).values(
        id=TEST_GOOGLE_USER_ID,
        email=TEST_GOOGLE_USER_EMAIL
    )
    code = 'fake_code'

    async with db_session as session:
        await session.execute(query)
        await session.commit()
        user_data = await auth_service.google_auth(code)
        login_user = (await session.execute(select(UserProfile).where(UserProfile.id == user_data.user_id))).scalar_one_or_none()
        session.expire_all()

    assert login_user.email == TEST_GOOGLE_USER_EMAIL
    assert user_data.user_id == TEST_GOOGLE_USER_ID


async def test_base_login__success(auth_service, db_session):
    username = 'test_username'
    password = 'test_password'
    hashed_password = auth_service.get_hashed_password(password=password)

    query = insert(UserProfile).values(
        username = username,
        password = hashed_password,
    )

    async with db_session as session:
        await session.execute(query)
        await session.commit()
        login_user = (
            await session.execute(select(UserProfile).where(UserProfile.username == username))).scalar_one_or_none()
        session.expire_all()

    user_data = await auth_service.login(username=username, password=password)

    assert login_user is not None
    assert user_data.user_id == login_user.id
