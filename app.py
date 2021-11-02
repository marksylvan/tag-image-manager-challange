from chalice import Chalice

from chalicelib.views.image_views import image_routes
from chalicelib.views.search_views import search_routes
from chalicelib.views.tag_views import tag_routes
from chalicelib.views.upload_views import upload_routes

app = Chalice(app_name="Tagged Image Manager")

app.register_blueprint(image_routes, url_prefix="/v1/images")
app.register_blueprint(search_routes, url_prefix="/v1/search")
app.register_blueprint(tag_routes, url_prefix="/v1/tags")
app.register_blueprint(upload_routes, url_prefix="/v1/upload")
