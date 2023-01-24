from typing import Any

from sqlalchemy.orm import Session


def pagination_query(
        *, model: Any, size: int, page: int, filter: Any | None = None, db: Session
    ) -> list[Any]:
    if filter is None:
        return db.query(model).limit(size).offset(size * page - size).all()
    return db.query(model).filter(filter).limit(size).offset(size * page - size).all()
