import re
from typing import Any

from fastapi import HTTPException, status

from sqlalchemy.orm import Session


def email_validator(email: str) -> bool:
    email_regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    return bool(re.fullmatch(email_regex, email))


def uniqe_validator(
        model: Any, obj: Any, field_name: str, db: Session
    ) -> HTTPException | None:
    if not getattr(obj, field_name, False):
        return None

    objects = db.query(model).all()
    for o in objects:
        if getattr(o, field_name) == getattr(obj, field_name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f'{field_name} field must be uniqe'
            )
