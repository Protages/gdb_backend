from fastapi import Response, status
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.schemas.genre_schemas import GenreCreate, GenreUpdate
from src.api_v1.exceptions import ObjectDoesNotExistException
from src.crud.queries import pagination_query
from src.models import models


def get_genre_by_id(db: Session, genre_id: int) -> models.Genre:
    db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if not db_genre:
        raise ObjectDoesNotExistException(obj_name='genre')
    return db_genre


def get_all_genres(db: Session, size: int, page: int) -> list[models.Genre]:
    db_genres = pagination_query(model=models.Genre, size=size, page=page, db=db)
    return db_genres


def create_genre(db: Session, genre: GenreCreate) -> models.Genre:
    db_genre = models.Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def update_genre(db: Session, genre_id: int, genre: GenreUpdate) -> models.Genre:
    db_genre = get_genre_by_id(db=db, genre_id=genre_id)
    update_data = jsonable_encoder(genre, exclude_unset=True)

    for field in jsonable_encoder(db_genre):
        if field in update_data:
            setattr(db_genre, field, update_data[field])

    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)

    return db_genre


def delete_genre(db: Session, genre_id: int):
    db_genre = get_genre_by_id(db=db, genre_id=genre_id)
    db.delete(db_genre)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
