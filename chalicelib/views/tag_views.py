from chalice import Blueprint

from chalicelib.authorizer import cognito_authorizer

tag_routes = Blueprint(__name__)


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
    return {"id": 0, "name": "a tag"}


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
