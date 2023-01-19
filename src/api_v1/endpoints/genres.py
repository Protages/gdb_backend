from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.models import models
from src.schemas.genre_schemas import Genre, GenreCreate, GenreUpdate
from src.crud import genre_crud
from src.api_v1.depends import get_db, oauth2_scheme, Pagination
from src.core import config
from src.core.security import (
    authenticate_user, 
    authenticate_user_by_token, 
    create_access_token
)

router = APIRouter(tags=['Genres'])


@router.get('/genre/{genre_id}', response_model=Genre)
async def read_genre_by_id(genre_id: int, db: Session = Depends(get_db)):
    genre = genre_crud.get_genre_by_id(db=db, genre_id=genre_id)
    return genre


@router.get('/genre/all/', response_model=list[Genre])
async def read_all_genres(paginator: Pagination = Depends(), db: Session = Depends(get_db)):
    genres = genre_crud.get_all_genres(db=db, size=paginator.size, page=paginator.page)
    return genres



@router.post('/genre', response_model=Genre)
async def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    genre = genre_crud.create_genre(db=db, genre=genre)
    return genre


@router.put('/genre/{genre_id}', response_model=Genre)
async def update_genre(genre_id: int, genre: GenreUpdate, db: Session = Depends(get_db)):
    genre = genre_crud.update_genre(db=db, genre_id=genre_id, genre=genre)
    return genre


@router.delete('/genre/{genre_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    response = genre_crud.delete_genre(db=db, genre_id=genre_id)
    return response

