import base64
import json
from pathlib import Path

from chalice.test import Client
from freezegun import freeze_time
from sqlalchemy.orm.session import Session

from app import app
from chalicelib.models import Image
from tests.helpers import dict_assert


@freeze_time("2021-11-03 21:00:00")
def test_upload(db_session: Session, snapshot):
    image_data = Path("tests/samples/image-00000.dcm").read_bytes()
    image_b64_bytes = base64.b64encode(image_data)
    image_b64_str = image_b64_bytes.decode("utf-8")

    with Client(app) as client:
        response = client.http.post(
            "/v1/upload",
            headers={"Content-Type": "application/json"},
            body=json.dumps(
                {
                    "filename": "image-00000.dcm",
                    "image_data": image_b64_str,
                    "tags": ["foo", "bar"],
                }
            ),
        ).json_body
        dict_assert(response, snapshot)

        image_id = response["id"]
        image: Image = db_session.query(Image).filter_by(id=image_id).first()
        assert image.filename == "image-00000.dcm"
        assert image.upload_timestamp is not None
        assert [t.name for t in image.tags] == ["foo", "bar"]
