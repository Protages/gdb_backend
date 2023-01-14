from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.models import models
from src.schemas.game_schemas import Game, GameCreate, GameUpdate
from src.crud import game_crud
from src.api_v1.depends import get_db, oauth2_scheme
from src.core import config
from src.core.security import (
    authenticate_user, 
    authenticate_user_by_token, 
    create_access_token
)

router = APIRouter(tags=['Games'])


@router.get('/game/{game_id}', response_model=Game)
async def read_game_by_id(game_id: int, db: Session = Depends(get_db)):
    db_game = game_crud.get_game_by_id(db=db, game_id=game_id)
    if not db_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Object does not exist"
        )
    return db_game


@router.post('/game', response_model=Game)
async def create_game(game: GameCreate, db: Session = Depends(get_db)):
    db_game = game_crud.create_game(db=db, game=game)
    return db_game


@router.put('/game/{game_id}', response_model=Game)
async def update_game(game_id: int, game: GameUpdate, db: Session = Depends(get_db)):
    db_game = game_crud.update_game(db=db, game_id=game_id, game=game)
    return db_game


@router.delete('/game/{game_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id: int, db: Session = Depends(get_db)):
    response = game_crud.delete_game(db=db, game_id=game_id)
    return response
