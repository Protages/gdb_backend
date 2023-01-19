from fastapi import Response, status
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.schemas.platform_schemas import PlatformCreate, PlatformUpdate
from src.api_v1.exceptions import ObjectDoesNotExistException
from src.crud.queries import pagination_query
from src.models import models


def get_platform_by_id(db: Session, platform_id: int) -> models.Platform:
    db_platform = db.query(models.Platform).\
        filter(models.Platform.id == platform_id).first()
    if not db_platform:
        raise ObjectDoesNotExistException(obj_name='platform')
    return db_platform


def get_all_platforms(db: Session, size: int, page: int) -> list[models.Platform]:
    db_platforms = pagination_query(model=models.Platform, size=size, page=page, db=db)
    return db_platforms


def create_platform(db: Session, platform: PlatformCreate) -> models.Platform:
    db_platform = models.Platform(**platform.dict())
    db.add(db_platform)
    db.commit()
    db.refresh(db_platform)
    return db_platform


def update_platform(
        db: Session, platform_id: int, platform: PlatformUpdate
    ) -> models.Platform:
    db_platform = get_platform_by_id(db=db, platform_id=platform_id)
    update_data = jsonable_encoder(platform, exclude_unset=True)

    for field in jsonable_encoder(db_platform):
        if field in update_data:
            setattr(db_platform, field, update_data[field])

    db.add(db_platform)
    db.commit()
    db.refresh(db_platform)

    return db_platform


def delete_platform(db: Session, platform_id: int):
    db_platform = get_platform_by_id(db=db, platform_id=platform_id)
    db.delete(db_platform)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
