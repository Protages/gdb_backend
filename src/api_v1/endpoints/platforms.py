from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.models import models
from src.schemas.platform_schemas import Platform, PlatformCreate, PlatformUpdate
from src.crud import platform_crud
from src.api_v1.depends import get_db, oauth2_scheme, Pagination
from src.core import config
from src.core.security import (
    authenticate_user, 
    authenticate_user_by_token, 
    create_access_token
)

router = APIRouter(tags=['Platforms'])


@router.get('/platform/{platform_id}', response_model=Platform)
async def read_platform_by_id(platform_id: int, db: Session = Depends(get_db)):
    db_platform = platform_crud.get_platform_by_id(db=db, platform_id=platform_id)
    return db_platform


@router.get('/platform/all/', response_model=list[Platform])
async def read_all_platform(
        paginator: Pagination = Depends(), db: Session = Depends(get_db)
    ):
    db_platforms = platform_crud.get_all_platforms(
        db=db, size=paginator.size, page=paginator.page
    )
    return db_platforms


@router.post('/platform', response_model=Platform)
async def create_platform(platform: PlatformCreate, db: Session = Depends(get_db)):
    db_platform = platform_crud.create_platform(db=db, platform=platform)
    return db_platform


@router.put('/platform/{platform_id}', response_model=Platform)
async def update_platform(
        platform_id: int, platform: PlatformUpdate, db: Session = Depends(get_db)
    ):
    db_platform = platform_crud.update_platform(
        db=db, platform_id=platform_id, platform=platform
    )
    return db_platform


@router.delete('/platform/{platform_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_platform(platform_id: int, db: Session = Depends(get_db)):
    response = platform_crud.delete_platform(db=db, platform_id=platform_id)
    return response
