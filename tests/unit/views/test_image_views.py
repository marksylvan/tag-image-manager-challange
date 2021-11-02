import pytest
from app import app
from chalice.test import Client
from tests.helpers import dict_assert


def test_images(snapshot):
    with Client(app) as client:
        response = client.http.get("/v1/images")
        dict_assert(response.json_body, snapshot)


def test_post_image(snapshot):
    with Client(app) as client:
        response = client.http.post("/v1/images")
        dict_assert(response.json_body, snapshot)


def test_image(snapshot):
    with Client(app) as client:
        response = client.http.get("/v1/images/1")
        dict_assert(response.json_body, snapshot)


def test_image_update(snapshot):
    with Client(app) as client:
        response = client.http.put("/v1/images/1")
        dict_assert(response.json_body, snapshot)


def test_image_delete(snapshot):
    with Client(app) as client:
        response = client.http.delete("/v1/images/1")
        dict_assert(response.json_body, snapshot)
