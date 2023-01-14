from fastapi import Response, status

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.schemas.category_schemas import CategoryCreate, CategoryUpdate
from src.models import models


def get_category_by_id(db: Session, category_id: int) -> models.Category:
    db_category = db.query(models.Category)\
        .filter(models.Category.id == category_id).first()
    return db_category


def create_category(db: Session, category: CategoryCreate) -> models.Category:
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(
        db: Session, category_id: int, category: CategoryUpdate
    ) -> models.Category:
    res = db.execute(
        Update(models.Category)
        .where(models.Category.id == category_id)
        .values(**category.dict(exclude_unset=True))
    )
    db.commit()
    db_category = get_category_by_id(db=db, category_id=category_id)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = get_category_by_id(db=db, category_id=category_id)
    db.delete(db_category)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
