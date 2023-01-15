import re
from typing import Any

from fastapi import HTTPException, status

from sqlalchemy.orm import Session


def email_validator(email: str) -> bool:
    email_regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    return bool(re.fullmatch(email_regex, email))


def unique_validator(
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


def unique_together_validator(
        model: Any, 
        obj: Any, 
        first_field_name: str, 
        second_field_name: str, 
        db: Session, 
        field_names_with_id: bool = False
    ) -> HTTPException | None:
    obj_first_field_name = first_field_name
    obj_second_field_name = second_field_name
    
    if field_names_with_id:
        regex_for_id = '([A-Za-z0-9-]+(_id))'
        if bool(re.fullmatch(regex_for_id, first_field_name)):
            obj_first_field_name = first_field_name[:-3]
        if bool(re.fullmatch(regex_for_id, second_field_name)):
            obj_second_field_name = second_field_name[:-3]

    if not (getattr(obj, obj_first_field_name, False) and getattr(obj, obj_second_field_name, False)):
        return None
    
    objects = db.query(model).all()
    for o in objects:
        is_first_fields_equal = getattr(o, first_field_name) == getattr(obj, obj_first_field_name)
        is_second_fields_equal = getattr(o, second_field_name) == getattr(obj, obj_second_field_name)
        if is_first_fields_equal and is_second_fields_equal:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f'{obj_first_field_name} and {obj_second_field_name} field must be unique together'
            )
