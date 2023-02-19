from typing import Any

from sqlalchemy.orm import Session


def pagination_query(
    *, model: Any, size: int, page: int, filter: Any | None = None, db: Session
) -> list[Any]:
    '''
    Return a list of objects by the received size and page,
    filter is used in a database query
    '''
    if filter is None:
        return db.query(model).limit(size).offset(size * page - size).all()
    return db.query(model).filter(filter).limit(size).offset(size * page - size).all()
