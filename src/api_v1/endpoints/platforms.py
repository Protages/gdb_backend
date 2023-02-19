from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.schemas.platform_schemas import Platform, PlatformCreate, PlatformUpdate
from src.crud import platform_crud
from src.api_v1.depends import get_db, Pagination


router = APIRouter(prefix='/platform', tags=['Platforms'])


@router.get('/{platform_id}', response_model=Platform)
async def read_platform_by_id(platform_id: int, db: Session = Depends(get_db)):
    db_platform = platform_crud.get_platform_by_id(db=db, platform_id=platform_id)
    return db_platform


@router.get('/', response_model=list[Platform])
async def read_all_platform(
    paginator: Pagination = Depends(), db: Session = Depends(get_db)
):
    db_platforms = platform_crud.get_all_platforms(
        db=db, size=paginator.size, page=paginator.page
    )
    return db_platforms


@router.post('/', response_model=Platform, status_code=status.HTTP_201_CREATED)
async def create_platform(platform: PlatformCreate, db: Session = Depends(get_db)):
    db_platform = platform_crud.create_platform(db=db, platform=platform)
    return db_platform


@router.put('/{platform_id}', response_model=Platform)
async def update_platform(
    platform_id: int, platform: PlatformUpdate, db: Session = Depends(get_db)
):
    db_platform = platform_crud.update_platform(
        db=db, platform_id=platform_id, platform=platform
    )
    return db_platform


@router.delete('/{platform_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_platform(platform_id: int, db: Session = Depends(get_db)):
    response = platform_crud.delete_platform(db=db, platform_id=platform_id)
    return response
