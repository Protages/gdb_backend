from fastapi import Response, status

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.schemas.genre_schemas import GenreCreate, GenreUpdate
from src.models import models


def get_genre_by_id(db: Session, genre_id: int) -> models.Genre:
    db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    return db_genre


def create_genre(db: Session, genre: GenreCreate) -> models.Genre:
    db_genre = models.Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def update_genre(db: Session, genre_id: int, genre: GenreUpdate) -> models.Genre:
    res = db.execute(
        Update(models.Genre)
        .where(models.Genre.id == genre_id)
        .values(**genre.dict(exclude_unset=True))
    )
    db.commit()
    db_genre = get_genre_by_id(db=db, genre_id=genre_id)
    return db_genre


def delete_genre(db: Session, genre_id: int):
    db_genre = get_genre_by_id(db=db, genre_id=genre_id)
    db.delete(db_genre)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
