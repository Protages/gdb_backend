from fastapi import Response, status

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.models import models
from src.schemas.role_schemas import RoleCreate, RoleUpdate, Role


def get_role_by_id(db: Session, role_id: int) -> models.Role:
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def create_role(db: Session, role: RoleCreate) -> models.Role:
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def update_role(db: Session, role_id: int, role: RoleUpdate) -> models.Role:
    update_data = role.dict(exclude_unset=True)
    res = db.execute(
        Update(models.Role)
        .where(models.Role.id == role_id)
        .values(**update_data)
    )
    db.commit()
    db_role = get_role_by_id(db=db, role_id=role_id)
    return db_role


def delete_role(db: Session, role_id: int):
    db_role = get_role_by_id(db=db, role_id=role_id)
    db.delete(db_role)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
