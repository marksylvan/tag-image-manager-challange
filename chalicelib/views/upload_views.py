from chalice import Blueprint

from chalicelib.authorizer import cognito_authorizer

upload_routes = Blueprint(__name__)


@upload_routes.route(
    "/", methods=["GET"], authorizer=cognito_authorizer, cors=True
)
def upload_images():
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
