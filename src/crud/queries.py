from typing import Any

from sqlalchemy.orm import Session


def pagination_query(model: Any, size: int, page: int, db: Session) -> list[Any]:
    return db.query(model).limit(size).offset(size * page - size).all()
