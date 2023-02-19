from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.schemas.genre_schemas import Genre, GenreCreate, GenreUpdate
from src.crud import genre_crud
from src.api_v1.depends import get_db, Pagination


router = APIRouter(prefix='/genre', tags=['Genres'])


@router.get('/{genre_id}', response_model=Genre)
async def read_genre_by_id(genre_id: int, db: Session = Depends(get_db)):
    genre = genre_crud.get_genre_by_id(db=db, genre_id=genre_id)
    return genre


@router.get('/', response_model=list[Genre])
async def read_all_genres(
    paginator: Pagination = Depends(), db: Session = Depends(get_db)
):
    genres = genre_crud.get_all_genres(db=db, size=paginator.size, page=paginator.page)
    return genres


@router.post('/', response_model=Genre, status_code=status.HTTP_201_CREATED)
async def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    genre = genre_crud.create_genre(db=db, genre=genre)
    return genre


@router.put('/{genre_id}', response_model=Genre)
async def update_genre(
    genre_id: int, genre: GenreUpdate, db: Session = Depends(get_db)
):
    genre = genre_crud.update_genre(db=db, genre_id=genre_id, genre=genre)
    return genre


@router.delete('/{genre_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    response = genre_crud.delete_genre(db=db, genre_id=genre_id)
    return response
