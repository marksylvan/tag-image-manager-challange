from app import app
from chalice.test import Client
from tests.helpers import dict_assert


def test_search(snapshot):
    with Client(app) as client:
        response = client.http.get("/v1/search")
        dict_assert(response.json_body, snapshot)
