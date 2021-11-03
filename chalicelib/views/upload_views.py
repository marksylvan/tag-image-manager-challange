import base64
import typing

from chalice import Blueprint
from sqlalchemy.sql import base

from chalicelib.authorizer import cognito_authorizer
from chalicelib.db import get_session
from chalicelib.models import Image
from chalicelib.validation import (
    ValidationParam,
    validate_payload,
    validate_query_params,
)
from chalicelib.views.helpers import retrieve_tag_records

upload_routes = Blueprint(__name__)

POST_PARAMS = [
    ValidationParam("filename", str, True, min_len=3, max_len=160),
    ValidationParam("image_data", str, True, min=1),
    ValidationParam("tags", typing.List, True, list_type=str),
]


@upload_routes.route(
    "/", methods=["POST"], authorizer=cognito_authorizer, cors=True
)
def upload_images():
    validate_payload(upload_routes, POST_PARAMS)
    payload = upload_routes.current_request.json_body
    session = get_session()
    filename = payload["filename"]
    tag_records = retrieve_tag_records(payload["tags"], session)
    image_data = base64.b64decode(payload["image_data"])

    # TODO: grab userid from cognito token in prod environment
    image = Image.from_upload(
        session, "user-id", filename, image_data, tag_records
    )

    return image.to_payload()
