import pytest

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.settings import settings as s
from app.infrastructure.database import Base


@pytest.fixture
def settings():
    s.DB_NAME = 'pomodoro-test'
    return s


engine = create_async_engine(
    url='postgresql+asyncpg://postgres_user:postgres_password@localhost:5430/pomodoro-test',
    future=True,
    echo=True,
    pool_pre_ping=True
)


@pytest_asyncio.fixture(scope='function', autouse=True)
async def async_db_engine(event_loop):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope='function')
async def db_session(async_db_engine):
    async_session = async_sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        class_=AsyncSession,
    )

    async with async_session() as session:
        await session.begin()

        yield session

        await session.rollback()