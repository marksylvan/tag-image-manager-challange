from datetime import date
from unittest.mock import MagicMock

import pytest
from chalice.app import BadRequestError, Chalice, Request
from chalicelib.validation import (
    ValidationParam,
    validate_payload,
    validate_query_params,
)


def test_basic_types_valid():
    mock_request = MagicMock(spec_set=Request)
    mock_log = MagicMock()
    mock_app = MagicMock(Chalice)
    mock_app.current_request = mock_request
    mock_app.log = mock_log

    # valid, required and present
    mock_request.json_body = {
        "int": 1,
        "float": 123.45,
        "str": "hello world",
        "bool": True,
    }

    specs = [
        ValidationParam("int", int, True),
        ValidationParam("float", float, True),
        ValidationParam("str", str, True),
        ValidationParam("bool", bool, True),
    ]
    validate_payload(mock_app, specs)


@pytest.mark.parametrize(
    "test_input",
    [
        None,
        {"int": "1", "float": 123.45, "str": "hello world", "bool": True},
        {"int": 1, "float": "123.45", "str": "hello world", "bool": True},
        {"int": 1, "float": 123.45, "str": 6, "bool": True},
        {"int": 1, "float": 123.45, "str": "hello world", "bool": "True"},
    ],
)
def test_basic_types_invalid(test_input):
    mock_request = MagicMock(spec_set=Request)
    mock_log = MagicMock()
    mock_app = MagicMock(Chalice)
    mock_app.current_request = mock_request
    mock_app.log = mock_log

    # valid, required and present
    mock_request.json_body = test_input
    specs = [
        ValidationParam("int", int, True),
        ValidationParam("float", float, True),
        ValidationParam("str", str, True),
        ValidationParam("bool", bool, True),
    ]
    with pytest.raises(BadRequestError):
        validate_payload(mock_app, specs)


def test_missing_field():
    mock_request = MagicMock(spec_set=Request)
    mock_log = MagicMock()
    mock_app = MagicMock(Chalice)
    mock_app.current_request = mock_request
    mock_app.log = mock_log

    # valid, required and present
    mock_request.json_body = {"int": 1, "float": 123.45, "str": "hello world"}
    specs = [
        ValidationParam("int", int, True),
        ValidationParam("float", float, True),
        ValidationParam("str", str, True),
        ValidationParam("bool", bool, True),
    ]
    with pytest.raises(BadRequestError):
        validate_payload(mock_app, specs)


@pytest.mark.parametrize(
    "test_input",
    [
        None,
        {
            "int": 1,
            "float": "123.45",
            "str": "hello world",
            "bool": True,
            "date": "2020-12-07",
        },
        {
            "int": 1,
            "float": 123.45,
            "str": 6,
            "bool": True,
            "date": "2020-12-07",
        },
        {
            "int": 1,
            "float": 123.45,
            "str": "hello world",
            "bool": "True",
            "date": "2020-12-07",
        },
        {
            "int": 1,
            "float": 123.45,
            "str": "hello world",
            "bool": True,
            "date": "foo",
        },
    ],
)
def test_query_param_validation(test_input):
    mock_request = MagicMock()
    mock_log = MagicMock()
    mock_app = MagicMock(Chalice)
    mock_app.current_request = mock_request
    mock_app.log = mock_log

    # valid, required and present
    mock_request.query_params = test_input
    specs = [
        ValidationParam("int", int, True),
        ValidationParam("float", float, True),
        ValidationParam("str", str, True),
        ValidationParam("bool", bool, True),
        ValidationParam("date", date, True),
    ]
    with pytest.raises(BadRequestError):
        validate_query_params(mock_app, specs)


def test_ints_with_limits():
    mock_request = MagicMock(spec_set=Request)
    mock_log = MagicMock()
    mock_app = MagicMock(Chalice)
    mock_app.current_request = mock_request
    mock_app.log = mock_log

    # valid, required and present
    mock_request.json_body = {"int": 1}

    spec = ValidationParam("int", int, True, min=2019)
    mock_request.json_body = {"int": 2019}
    validate_payload(mock_app, [spec])
    mock_request.json_body = {"int": 2020}
    validate_payload(mock_app, [spec])

    mock_request.json_body = {"int": 2018}
    with pytest.raises(BadRequestError):
        validate_payload(mock_app, [spec])

    spec = ValidationParam("int", int, True, min=1, max=12)
    mock_request.json_body = {"int": 1}
    validate_payload(mock_app, [spec])
    mock_request.json_body = {"int": 12}
    validate_payload(mock_app, [spec])

    mock_request.json_body = {"int": 0}
    with pytest.raises(BadRequestError):
        validate_payload(mock_app, [spec])

    mock_request.json_body = {"int": 13}
    with pytest.raises(BadRequestError):
        validate_payload(mock_app, [spec])


def test_strings_max_min_len():
    mock_request = MagicMock(spec_set=Request)
    mock_log = MagicMock()
    mock_app = MagicMock(Chalice)
    mock_app.current_request = mock_request
    mock_app.log = mock_log

    spec = ValidationParam("str", str, True, min_len=0)
    mock_request.json_body = {"str": "foo"}
    validate_payload(mock_app, [spec])

    mock_request.json_body = {"str": None}
    with pytest.raises(BadRequestError):
        validate_payload(mock_app, [spec])

    # compulsory and cannot be empty
    spec = ValidationParam("str", str, True, min_len=1)

    mock_request.json_body = {"str": ""}
    with pytest.raises(BadRequestError):
        validate_payload(mock_app, [spec])

    mock_request.json_body = {"str": "     "}
    with pytest.raises(BadRequestError):
        validate_payload(mock_app, [spec])

    mock_request.json_body = {"str": "\n\n\n\n\t\n"}
    with pytest.raises(BadRequestError):
        validate_payload(mock_app, [spec])

    mock_request.json_body = {"str": "  .   "}
    validate_payload(mock_app, [spec])

    # max len tests
    spec = ValidationParam("str", str, True, max_len=3)

    mock_request.json_body = {"str": "abc"}
    validate_payload(mock_app, [spec])

    mock_request.json_body = {"str": "    abc   "}
    validate_payload(mock_app, [spec])

    mock_request.json_body = {"str": "abcd"}
    with pytest.raises(BadRequestError):
        validate_payload(mock_app, [spec])

    # both combined
    spec = ValidationParam("str", str, True, min_len=2, max_len=3)

    mock_request.json_body = {"str": "ab"}
    validate_payload(mock_app, [spec])

    mock_request.json_body = {"str": "abc"}
    validate_payload(mock_app, [spec])

    mock_request.json_body = {"str": "    abc   "}
    validate_payload(mock_app, [spec])

    mock_request.json_body = {"str": "a"}
    with pytest.raises(BadRequestError):
        validate_payload(mock_app, [spec])

    mock_request.json_body = {"str": "abcd"}
    with pytest.raises(BadRequestError):
        validate_payload(mock_app, [spec])


def test_query_param_optional_with_none():
    mock_request = MagicMock()
    mock_log = MagicMock()
    mock_app = MagicMock(Chalice)
    mock_app.current_request = mock_request
    mock_app.log = mock_log

    # valid, required and present
    mock_request.query_params = None
    specs = [
        ValidationParam("int", int, required=False),
    ]
    validate_query_params(mock_app, specs)
