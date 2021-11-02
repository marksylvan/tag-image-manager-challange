from chalice import Blueprint

from chalicelib.authorizer import cognito_authorizer

image_routes = Blueprint(__name__)


@image_routes.route(
    "/", methods=["GET"], authorizer=cognito_authorizer, cors=True
)
def get_images():
    return {
        "results": [{"id": 0, "name": "string"}],
        "meta": {
            "current_page": 0,
            "has_more_pages": False,
            "total_results": 0,
        },
    }


@image_routes.route(
    "/", methods=["POST"], authorizer=cognito_authorizer, cors=True
)
def create_image():
    return {"id": 0, "upload_url": "some url"}


@image_routes.route(
    "/{image_id}", methods=["GET"], authorizer=cognito_authorizer, cors=True
)
def get_image(image_id: str):
    return {
        "id": 0,
        "created_by": "foo",
        "created_timestamp": 0,
        "filename": "foo.dcm",
        "size": 0,
        "tags": [{"id": 0, "name": "thing"}],
        "uploaded_timestamp": None,
        "url": None,
    }


@image_routes.route(
    "/{image_id}", methods=["PUT"], authorizer=cognito_authorizer, cors=True
)
def update_image(image_id: str):
    return {}


@image_routes.route(
    "/{image_id}", methods=["DEL"], authorizer=cognito_authorizer, cors=True
)
def delete_image(image_id: str):
    return {}
