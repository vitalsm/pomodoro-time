from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

Session = sessionmaker(create_engine(settings.database_url))


def get_db_session() -> Session:
    return Session
