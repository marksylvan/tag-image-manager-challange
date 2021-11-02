import typing

from chalice import BadRequestError, Blueprint, NotFoundError
from sqlalchemy.orm.session import Session

from chalicelib.authorizer import cognito_authorizer
from chalicelib.db import get, get_or_create, get_session
from chalicelib.models import Tag
from chalicelib.validation import ValidationParam, validate_payload

tag_routes = Blueprint(__name__)

POST_PARAMS = [ValidationParam("name", str, True, min_len=3, max_len=160)]


def _tag_by_id(tag_id: typing.Any, session: Session) -> Tag:
    try:
        tag_id = int(tag_id)
    except ValueError:
        raise BadRequestError(f"Could not cast {tag_id} to int")

    tag: typing.Optional[Tag] = get(session, Tag, tag_id)

    if tag:
        return tag

    raise NotFoundError()


def _validate_and_extract_upsert_params(
    tag_routes: Blueprint,
) -> typing.Mapping[str, typing.Any]:
    validate_payload(tag_routes, POST_PARAMS)

    return tag_routes.current_request.json_body


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
    payload = _validate_and_extract_upsert_params(tag_routes)
    session = get_session()
    tag: Tag = get_or_create(session, Tag, name=payload["name"])
    return tag.to_payload()


@tag_routes.route(
    "/{tag_id}", methods=["GET"], authorizer=cognito_authorizer, cors=True
)
def get_tag(tag_id: str):
    session = get_session()
    return _tag_by_id(tag_id, session).to_payload()


@tag_routes.route(
    "/{tag_id}", methods=["PUT"], authorizer=cognito_authorizer, cors=True
)
def update_tag(tag_id: str):
    payload = _validate_and_extract_upsert_params(tag_routes)
    session = get_session()
    tag: Tag = _tag_by_id(tag_id, session)
    tag.name = payload["name"]
    session.add(tag)
    session.commit()
    return tag.to_payload()


@tag_routes.route(
    "/{tag_id}", methods=["DELETE"], authorizer=cognito_authorizer, cors=True
)
def delete_tag(tag_id: str):
    session = get_session()
    tag: Tag = _tag_by_id(tag_id, session)
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
