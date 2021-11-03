import typing
from dataclasses import dataclass

from chalice import BadRequestError, Chalice
from chalice.app import Request


@dataclass
class ValidationParam:
    field_name: str
    field_type: typing.Any
    required: bool = False
    # numeric fields0
    min: typing.Union[None, int, float] = None
    max: typing.Union[None, int, float] = None

    # str fields
    min_len: typing.Optional[int] = None
    max_len: typing.Optional[int] = None

    # lists
    list_type: typing.Optional[typing.Any] = None

    def __post_init__(self):
        if self.field_type == str and self.max_len is not None:
            if self.max_len < 1:
                raise ValueError("String field cannot have max_len < 1")

            if self.min_len is not None and self.min_len > self.max_len:
                raise ValueError(
                    "String field cannot have min_len cannot be > max_len"
                )


def _is_numeric_field(field_val):
    return isinstance(field_val, int) or isinstance(field_val, float)


def _validate(
    data: typing.Mapping[str, typing.Any],
    specs: typing.List[ValidationParam],
    from_querystr=False,
) -> typing.List[str]:
    """Runs validation specs over data and returns errors list"""
    errors: typing.List[str] = []
    for spec in specs:
        if spec.required and spec.field_name not in data.keys():
            errors.append(f"{spec.field_name} missing")
            continue

        if spec.field_name in data.keys():
            field_val = data[spec.field_name]

            if from_querystr and spec.field_type == int:
                try:
                    field_val = int(data[spec.field_name])
                except ValueError:
                    errors.append(f"{spec.field_name} expected integer")

            if not isinstance(field_val, spec.field_type):
                errors.append(
                    f"{spec.field_name} invalid type, expecting {spec.field_type}, got {type(data[spec.field_name])}"  # noqa: E501
                )

            if isinstance(field_val, typing.List):
                passes = all(
                    [isinstance(v, spec.list_type) for v in field_val]
                )

                if not passes:
                    errors.append(
                        f"each member of {spec.field_name} must be {spec.list_type}"  # noqa: E501
                    )

            if _is_numeric_field(field_val) and spec.min is not None:
                if field_val < spec.min:
                    errors.append(
                        f"{spec.field_name} less then min {field_val} < {spec.min}"  # noqa: E501
                    )

            if _is_numeric_field(field_val) and spec.max is not None:
                if field_val > spec.max:
                    errors.append(
                        f"{spec.field_name} greater then max {field_val} > {spec.max}"  # noqa: E501
                    )

            if isinstance(field_val, str) and spec.min_len is not None:
                if len(field_val.strip()) < spec.min_len:
                    errors.append(
                        f"{spec.field_name} minimum length: {spec.min_len}"  # noqa: E501
                    )

            if isinstance(field_val, str) and spec.max_len is not None:
                if len(field_val.strip()) > spec.max_len:
                    errors.append(
                        f"{spec.field_name} maximum length: {spec.max_len}"  # noqa: E501
                    )

    return errors


def validate_payload(
    app: Chalice,
    specs: typing.List[ValidationParam],
) -> None:
    """
    Immediately raises a bad request if required field
    is missing, or field is incorrect type
    """
    current_request: Request = app.current_request
    if current_request.json_body is None:
        app.log.warn("Request validation failed: no json data")
        raise BadRequestError("no json data")

    data: typing.Dict[str, typing.Any] = current_request.json_body

    if data is None:
        app.log.warn("Request validation failed: root data element is empty")
        raise BadRequestError("Root 'data' element empty")

    errors = _validate(data, specs)

    if len(errors) > 0:
        app.log.warn({"msg": "Request validation failed", "errors": errors})

        raise BadRequestError(f"Validation failed: {errors}")


def validate_query_params(
    app: Chalice,
    specs: typing.List[ValidationParam],
) -> None:
    """
    Immediately raises a bad request if required field is missing,
    or field is incorrect type
    """
    current_request: Request = app.current_request
    if current_request.query_params is None:
        if any([s.required for s in specs]):
            app.log.warn("Request validation failed: query_params missing")
            raise BadRequestError("query_params: query_params missing")

        return

    query_params: typing.Dict[str, typing.Any] = current_request.query_params
    errors = _validate(query_params, specs, from_querystr=True)

    if len(errors) > 0:
        app.log.warn(f"Request validation failed: {errors}")
        raise BadRequestError(f"Validation failed: {errors}")
