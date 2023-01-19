from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.models import models
from src.schemas.category_schemas import (
    Category,
    CategoryCreate,
    CategoryUpdate,
    CategoryUpdateGame
)
from src.crud import category_crud
from src.api_v1.depends import get_db, oauth2_scheme, Pagination
from src.core import config
from src.core.security import (
    authenticate_user, 
    authenticate_user_by_token, 
    create_access_token
)

router = APIRouter(tags=['Categories'])


@router.get('/category/{category_id}', response_model=Category)
async def read_category_by_id(category_id: int, db: Session = Depends(get_db)):
    db_category = category_crud.get_category_by_id(db=db, category_id=category_id)
    return db_category


@router.get('/category/all/', response_model=list[Category])
async def read_all_categories(
        paginator: Pagination = Depends(), db: Session = Depends(get_db)
    ):
    db_categories = category_crud.get_all_categories(
        db=db, size=paginator.size, page=paginator.page
    )
    return db_categories


@router.get('/category/all/{user_id}', response_model=list[Category])
async def read_all_categories_by_user_id(
        user_id: int, paginator: Pagination = Depends(), db: Session = Depends(get_db)
    ):
    db_categories = category_crud.get_categories_by_user_id(
        db=db, size=paginator.size, page=paginator.page, user_id=user_id
    )
    return db_categories


@router.post('/category', response_model=Category)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = category_crud.create_category(db=db, category=category)
    return db_category


@router.put('/category/{category_id}', response_model=Category)
async def update_category(
        category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)
    ):
    db_category = category_crud.update_category(
        db=db, category_id=category_id, category=category
    )
    return db_category


@router.delete('/category/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    response = category_crud.delete_category(db=db, category_id=category_id)
    return response


@router.put('/category/{category_id}/games', response_model=Category)
async def add_game_to_category(
        category_id: int, game: CategoryUpdateGame, db: Session = Depends(get_db)
    ):
    db_category = category_crud.add_game_to_category(
        db=db, catgory_id=category_id, game_id=game.game
    )
    return db_category


@router.delete('/category/{category_id}/games', response_model=Category)
async def remove_game_from_category(
        category_id: int, game: CategoryUpdateGame, db: Session = Depends(get_db)
    ):
    db_category = category_crud.remove_game_from_category(
        db=db, catgory_id=category_id, game_id=game.game
    )
    return db_category
