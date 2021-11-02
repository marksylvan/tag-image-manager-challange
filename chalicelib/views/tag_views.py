import typing

from chalice import Blueprint
from chalicelib.authorizer import cognito_authorizer
from chalicelib.db import get_session
from chalicelib.models import Tag
from chalicelib.validation import ValidationParam, validate_payload

tag_routes = Blueprint(__name__)

POST_PARAMS = [ValidationParam("name", str, True, min_len=3, max_len=160)]


@tag_routes.route(
    "/", methods=["GET"], authorizer=cognito_authorizer, cors=True
)
def get_tags():
    return {
        "results": [{"id": 0, "name": "a tag"}],
        "meta": {
            "current_page": 0,
            "has_more_pages": False,
            "total_results": 1,
        },
    }


@tag_routes.route(
    "/", methods=["POST"], authorizer=cognito_authorizer, cors=True
)
def create_tag():
    validate_payload(tag_routes, POST_PARAMS)

    payload: typing.Mapping[
        str, typing.Any
    ] = tag_routes.current_request.json_body
    session = get_session()
    new_tag = Tag(name=payload["name"])
    session.add(new_tag)
    session.commit()

    return {"id": new_tag.id, "name": new_tag.name}


@tag_routes.route(
    "/{tag_id}", methods=["GET"], authorizer=cognito_authorizer, cors=True
)
def get_tag(tag_id: str):
    return {"id": 0, "name": "a tag"}


@tag_routes.route(
    "/{tag_id}", methods=["PUT"], authorizer=cognito_authorizer, cors=True
)
def update_tag(tag_id: str):
    return {}


@tag_routes.route(
    "/{tag_id}", methods=["DEL"], authorizer=cognito_authorizer, cors=True
)
def delete_tag(tag_id: str):
    return {}


@tag_routes.route(
    "/{tag_id}/images",
    methods=["GET"],
    authorizer=cognito_authorizer,
    cors=True,
)
def get_tag_images(tag_id: str):
    return {
        "results": [{"id": 0, "name": "string"}],
        "meta": {
            "current_page": 0,
            "has_more_pages": False,
            "total_results": 0,
        },
    }
