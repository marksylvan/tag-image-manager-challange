import os
from typing import Mapping

import pytest


@pytest.fixture
def auth_headers() -> Mapping[str, str]:
    # return {"Authorization": os.environ["COGNITO_ID_TOKEN"]}
    # return {}
    return {
        "Authorization": {
            "Credential": os.environ["COGNITO_ID_TOKEN"],
            "Signature": os.environ["COGNITO_ID_TOKEN"],
            "SignedHeaders": [],
            "Date": "foo",
        }
    }
