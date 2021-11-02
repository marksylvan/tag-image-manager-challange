from unittest import mock

import pytest
from chalicelib.models import Base
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session, sessionmaker


@pytest.fixture
def db_engine() -> Engine:
    return create_engine(
        "sqlite+pysqlite:///:memory:", echo=False, future=True
    )


@pytest.fixture
def db_session(db_engine) -> Session:
    mock.patch("chalicelib.db.get_engine", db_engine)
    mock.patch("chalicelib.views.tag_views.get_engine", db_engine)
    Base.metadata.create_all(db_engine)
    Session = sessionmaker(bind=db_engine)
    session = Session()

    def return_session():
        return session

    with mock.patch("chalicelib.views.tag_views.get_session", return_session):
        yield Session()

    return session
