import typing

from chalice import BadRequestError, Blueprint, NotFoundError
from sqlalchemy.orm.session import Session

from chalicelib.authorizer import cognito_authorizer
from chalicelib.db import get, get_or_create, get_session
from chalicelib.models import Tag
from chalicelib.validation import (
    ValidationParam,
    validate_payload,
    validate_query_params,
)

tag_routes = Blueprint(__name__)

PAGE_PARAMS = [
    ValidationParam("limit", int, False, min=1, max=100),
    ValidationParam("page", int, False, min=0),
]

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
    validate_query_params(tag_routes, PAGE_PARAMS)
    payload: typing.Mapping[str, typing.Any] = (
        tag_routes.current_request.query_params or {}
    )
    session = get_session()

    current_page = int(payload.get("page", "0"))
    limit = int(payload.get("limit", "100"))
    total_results = session.query(Tag).count()
    start_index = current_page * limit
    end_index = min(total_results, current_page + 1 * limit)

    records = (
        session.query(Tag).order_by(Tag.name).slice(start_index, end_index)
    )

    return {
        "results": [record.to_payload() for record in records],
        "meta": {
            "current_page": current_page,
            "has_more_pages": total_results > end_index,
            "total_results": total_results,
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
