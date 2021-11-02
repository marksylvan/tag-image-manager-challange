import os

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from chalicelib.models import Base

engine = None


def create_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)


def get_engine() -> Engine:
    global engine

    if engine is None:
        engine = create_engine(os.environ["DB_URL"])

    return engine


def get_session() -> Session:
    Session = sessionmaker(bind=get_engine())
    return Session()
