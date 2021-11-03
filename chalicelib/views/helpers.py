import typing

from chalice.app import BadRequestError, NotFoundError
from sqlalchemy.orm.session import Session

from chalicelib.db import get
from chalicelib.models import Base


def model_by_id(
    id: typing.Any, session: Session, model: typing.Type[Base]
) -> Base:
    try:
        id = int(id)
    except ValueError:
        raise BadRequestError(f"Could not cast {id} to int")

    instance: typing.Optional[model] = get(session, model, id)

    if instance:
        return instance

    raise NotFoundError()


def simple_page_view(payload, session, model, sort_by):
    current_page = int(payload.get("page", "0"))
    limit = int(payload.get("limit", "100"))
    total_results = session.query(model).count()
    start_index = current_page * limit
    end_index = min(total_results, (current_page + 1) * limit)

    records = (
        session.query(model)
        .order_by(getattr(model, sort_by))
        .slice(start_index, end_index)
    )

    return {
        "results": [record.to_payload() for record in records],
        "meta": {
            "current_page": current_page,
            "has_more_pages": total_results > end_index,
            "total_results": total_results,
        },
    }
