import os
from pathlib import Path

import pytest
from chalicelib.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session, sessionmaker


@pytest.fixture(autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture()
def db_engine(autouse=True):
    tmp_db = Path("test.sqlite")

    if tmp_db.exists():
        tmp_db.unlink()

    db_url = f"sqlite+pysqlite:///{tmp_db.name}"
    os.environ["DB_URL"] = db_url
    db_engine = create_engine(db_url, echo=False, future=True)
    Base.metadata.create_all(db_engine)
    return db_engine


@pytest.fixture
def db_session(db_engine) -> Session:
    Session = sessionmaker(bind=db_engine)
    session = Session()

    return session
