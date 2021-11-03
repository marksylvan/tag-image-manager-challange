import typing

from chalice import Blueprint
from sqlalchemy.orm.session import Session

from chalicelib.authorizer import cognito_authorizer
from chalicelib.db import get_or_create, get_session
from chalicelib.models import Image, Tag
from chalicelib.validation import (
    ValidationParam,
    validate_payload,
    validate_query_params,
)
from chalicelib.views.helpers import model_by_id, simple_page_view
from chalicelib.views.tag_views import PAGE_PARAMS

image_routes = Blueprint(__name__)

UPDATE_PARAMS = [
    ValidationParam("tags", typing.List, True, list_type=str),
]

POST_PARAMS = [
    ValidationParam("filename", str, True, min_len=3, max_len=160),
    ValidationParam("size", int, True, min=1),
    ValidationParam("tags", typing.List, True, list_type=str),
]


def _retrieve_tag_records(new_tags: typing.List[str], session: Session):
    tag_records: typing.List[Tag] = []

    for tag in new_tags:
        tag_records.append(get_or_create(session, Tag, name=tag))
    return tag_records


@image_routes.route(
    "/", methods=["GET"], authorizer=cognito_authorizer, cors=True
)
def get_images():
    validate_query_params(image_routes, PAGE_PARAMS)
    payload: typing.Mapping[str, typing.Any] = (
        image_routes.current_request.query_params or {}
    )
    session = get_session()

    return simple_page_view(payload, session, Image, "created_timestamp")


@image_routes.route(
    "/", methods=["POST"], authorizer=cognito_authorizer, cors=True
)
def create_image():
    validate_payload(image_routes, UPDATE_PARAMS)
    payload = image_routes.current_request.json_body
    session = get_session()

    tag_records = _retrieve_tag_records(payload["tags"], session)

    # TODO: when deployed, grab the user id/name from their JWT
    return Image.prepare_upload_url(
        session, "user-name", payload["filename"], payload["size"], tag_records
    ).to_response()


@image_routes.route(
    "/{image_id}", methods=["GET"], authorizer=cognito_authorizer, cors=True
)
def get_image(image_id: str):
    session = get_session()
    return model_by_id(image_id, session, Image).to_payload()


@image_routes.route(
    "/{image_id}", methods=["PUT"], authorizer=cognito_authorizer, cors=True
)
def update_image(image_id: str):
    validate_payload(image_routes, UPDATE_PARAMS)
    new_tags: str = image_routes.current_request.json_body["tags"]

    session = get_session()
    image: Image = model_by_id(image_id, session, Image)
    tag_records = _retrieve_tag_records(new_tags, session)

    image.tags = tag_records
    session.commit()

    return image.to_payload()


@image_routes.route(
    "/{image_id}", methods=["DELETE"], authorizer=cognito_authorizer, cors=True
)
def delete_image(image_id: str):
    return {}
