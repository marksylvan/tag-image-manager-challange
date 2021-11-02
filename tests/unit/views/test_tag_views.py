import json

import pytest
from app import app
from chalice.test import Client
from chalicelib.models import Tag
from sqlalchemy.orm.session import Session
from tests.helpers import dict_assert


@pytest.fixture
def sample_tag(db_session: Session) -> int:
    tag = Tag(name="sample tag")
    db_session.add(tag)
    db_session.commit()
    return tag.id


def test_tags(db_session, sample_tag, snapshot):
    with Client(app) as client:
        response = client.http.get("/v1/tags")
        dict_assert(response.json_body, snapshot)


def test_create_tag(db_session, snapshot):
    with Client(app) as client:
        response = client.http.post(
            "/v1/tags",
            headers={"Content-Type": "application/json"},
            body=json.dumps({"name": "tag 1"}),
        )
        assert response.json_body["name"] == "tag 1"
        assert response.json_body["id"] == 1

        # tag with same name only created once
        response = client.http.post(
            "/v1/tags",
            headers={"Content-Type": "application/json"},
            body=json.dumps({"name": "tag 1"}),
        )
        assert response.json_body["name"] == "tag 1"
        assert response.json_body["id"] == 1

        assert db_session.query(Tag).where(Tag.name == "tag 1").count() == 1


def test_tag(sample_tag, snapshot):
    with Client(app) as client:
        # exists
        response = client.http.get(f"/v1/tags/{sample_tag}")
        dict_assert(response.json_body, snapshot)

        # not exist
        response = client.http.get(f"/v1/tags/0")
        assert response.json_body == {
            "Code": "NotFoundError",
            "Message": "NotFoundError: ",
        }

        # not an integer
        response = client.http.get(f"/v1/tags/foo bar baz")
        assert response.json_body == {
            "Code": "BadRequestError",
            "Message": "BadRequestError: Could not cast foo bar baz to int",
        }


def test_tag_update(db_session, sample_tag):
    with Client(app) as client:
        response = client.http.put(
            f"/v1/tags/{sample_tag}",
            headers={"Content-Type": "application/json"},
            body=json.dumps({"name": "sample tag x"}),
        )
        assert response.json_body == {"id": sample_tag, "name": "sample tag x"}


def test_tag_delete(db_session, sample_tag):
    with Client(app) as client:
        response = client.http.delete("/v1/tags/1")
        assert response.json_body == {}

        assert (
            db_session.query(Tag).where(Tag.name == "sample tag").count() == 0
        )


@pytest.mark.xfail()
def test_tag_images():
    # not implemented yet
    with Client(app) as client:
        response = client.http.get("/v1/tags/1/images")
        assert response.json_body == {}
