from app import app
from chalice.test import Client
from tests.helpers import dict_assert


def test_tags(snapshot):
    with Client(app) as client:
        response = client.http.get("/v1/tags")
        dict_assert(response.json_body, snapshot)


def test_post_tag(snapshot):
    with Client(app) as client:
        response = client.http.post("/v1/tags")
        dict_assert(response.json_body, snapshot)


def test_tag(snapshot):
    with Client(app) as client:
        response = client.http.get("/v1/tags/1")
        dict_assert(response.json_body, snapshot)


def test_tag_update(snapshot):
    with Client(app) as client:
        response = client.http.put("/v1/tags/1")
        dict_assert(response.json_body, snapshot)


def test_tag_delete(snapshot):
    with Client(app) as client:
        response = client.http.delete("/v1/tags/1")
        dict_assert(response.json_body, snapshot)
