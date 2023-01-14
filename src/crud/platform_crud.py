from fastapi import Response, status

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.schemas.platform_schemas import PlatformCreate, PlatformUpdate
from src.models import models


def get_platform_by_id(db: Session, platform_id: int) -> models.Platform:
    db_platform = db.query(models.Platform).\
        filter(models.Platform.id == platform_id).first()
    return db_platform


def create_platform(db: Session, platform: PlatformCreate) -> models.Platform:
    db_platform = models.Platform(**platform.dict())
    db.add(db_platform)
    db.commit()
    db.refresh(db_platform)
    return db_platform


def update_platform(
        db: Session, platform_id: int, platform: PlatformUpdate
    ) -> models.Platform:
    res = db.execute(
        Update(models.Platform)
        .where(models.Platform.id == platform_id)
        .values(**platform.dict(exclude_unset=True))
    )
    db.commit()
    db_platform = get_platform_by_id(db=db, platform_id=platform_id)
    return db_platform


def delete_platform(db: Session, platform_id: int):
    db_platform = get_platform_by_id(db=db, platform_id=platform_id)
    db.delete(db_platform)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
