from fastapi import Response, status
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.models import models
from src.api_v1.exceptions import ObjectDoesNotExistException
from src.schemas.role_schemas import RoleCreate, RoleUpdate, Role


def get_role_by_id(db: Session, role_id: int) -> models.Role:
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not db_role:
        raise ObjectDoesNotExistException(obj_name='role')
    return db_role


def create_role(db: Session, role: RoleCreate) -> models.Role:
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def update_role(db: Session, role_id: int, role: RoleUpdate) -> models.Role:
    db_role = get_role_by_id(db=db, role_id=role_id)
    update_data = jsonable_encoder(role, exclude_unset=True)

    for field in jsonable_encoder(db_role):
        if field in update_data:
            setattr(db_role, field, update_data[field])

    db.add(db_role)
    db.commit()
    db.refresh(db_role)

    return db_role


def delete_role(db: Session, role_id: int):
    db_role = get_role_by_id(db=db, role_id=role_id)
    db.delete(db_role)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
