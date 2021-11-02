from chalice import Blueprint

from chalicelib.authorizer import cognito_authorizer

search_routes = Blueprint(__name__)


@search_routes.route(
    "/images", methods=["GET"], authorizer=cognito_authorizer, cors=True
)
def search_images():
    return {
        "results": [{"id": 0, "name": "string"}],
        "meta": {
            "current_page": 0,
            "has_more_pages": False,
            "total_results": 0,
        },
    }
