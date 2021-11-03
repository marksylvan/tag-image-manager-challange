import typing

from chalice import Blueprint

from chalicelib.authorizer import cognito_authorizer
from chalicelib.db import get_or_create, get_session
from chalicelib.models import Tag
from chalicelib.validation import (
    ValidationParam,
    validate_payload,
    validate_query_params,
)
from chalicelib.views.helpers import model_by_id, simple_page_view

tag_routes = Blueprint(__name__)

POST_PARAMS = [ValidationParam("name", str, True, min_len=3, max_len=160)]
PAGE_PARAMS = [
    ValidationParam("limit", int, False, min=1, max=100),
    ValidationParam("page", int, False, min=0),
]


def _validate_and_extract_upsert_params(
    tag_routes: Blueprint,
) -> typing.Mapping[str, typing.Any]:
    validate_payload(tag_routes, POST_PARAMS)

    return tag_routes.current_request.json_body


@tag_routes.route(
    "/", methods=["GET"], authorizer=cognito_authorizer, cors=True
)
def get_tags():
    validate_query_params(tag_routes, PAGE_PARAMS)
    payload: typing.Mapping[str, typing.Any] = (
        tag_routes.current_request.query_params or {}
    )
    session = get_session()

    return simple_page_view(payload, session, Tag, "name")


@tag_routes.route(
    "/", methods=["POST"], authorizer=cognito_authorizer, cors=True
)
def create_tag():
    payload = _validate_and_extract_upsert_params(tag_routes)
    session = get_session()
    tag: Tag = get_or_create(session, Tag, name=payload["name"])
    return tag.to_payload()


@tag_routes.route(
    "/{tag_id}", methods=["GET"], authorizer=cognito_authorizer, cors=True
)
def get_tag(tag_id: str):
    session = get_session()
    return model_by_id(tag_id, session, Tag).to_payload()


@tag_routes.route(
    "/{tag_id}", methods=["PUT"], authorizer=cognito_authorizer, cors=True
)
def update_tag(tag_id: str):
    payload = _validate_and_extract_upsert_params(tag_routes)
    session = get_session()
    tag: Tag = model_by_id(tag_id, session, Tag)
    tag.name = payload["name"]
    session.add(tag)
    session.commit()
    return tag.to_payload()


@tag_routes.route(
    "/{tag_id}", methods=["DELETE"], authorizer=cognito_authorizer, cors=True
)
def delete_tag(tag_id: str):
    session = get_session()
    tag: Tag = model_by_id(tag_id, session, Tag)
    session.delete(tag)
    session.commit()
    return {}


@tag_routes.route(
    "/{tag_id}/images",
    methods=["GET"],
    authorizer=cognito_authorizer,
    cors=True,
)
def get_tag_images(tag_id: str):
    raise NotImplementedError
