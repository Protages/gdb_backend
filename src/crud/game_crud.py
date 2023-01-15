import datetime

from fastapi import Response, status, HTTPException
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.schemas.game_schemas import GameCreate, GameUpdate
from src.api_v1.exceptions import ObjectDoesNotExistException
from src.models import models
from src.crud import genre_crud, platform_crud


def get_game_by_id(db: Session, game_id: int) -> models.Game:
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not db_game:
        raise ObjectDoesNotExistException(obj_name='game')
    return db_game


def create_game(db: Session, game: GameCreate) -> models.Game:
    genres_id = game.genres
    platforms_id = game.platforms
    release = game.release

    create_data = jsonable_encoder(game, exclude={'genres', 'platforms'})
    create_data.update({'release': datetime.date.fromisoformat(str(release))})
    db_game = models.Game(**create_data)

    for genre_id in genres_id:
        genre = genre_crud.get_genre_by_id(db=db, genre_id=genre_id)
        db_game.genres.append(genre)

    for platform_id in platforms_id:
        platform = platform_crud.get_platform_by_id(db=db, platform_id=platform_id)
        db_game.platforms.append(platform)

    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return db_game


def update_game(db: Session, game_id: int, game: GameUpdate) -> models.Game:
    db_game = get_game_by_id(db=db, game_id=game_id)
    genres_id = game.genres
    platforms_id = game.platforms
    release = game.release

    update_data = jsonable_encoder(
        game, exclude={'genres', 'platforms'}, exclude_unset=True
    )
    if release:
        update_data.update({'release': datetime.date.fromisoformat(str(release))})

    for field in jsonable_encoder(db_game):
        if field in update_data:
            setattr(db_game, field, update_data[field])

    if genres_id:
        db_game.genres.clear()
        for genre_id in genres_id:
            genre = genre_crud.get_genre_by_id(db=db, genre_id=genre_id)
            db_game.genres.append(genre)

    if platforms_id:
        db_game.platforms.clear()
        for platform_id in platforms_id:
            platform = platform_crud.get_platform_by_id(db=db, platform_id=platform_id)
            db_game.platforms.append(platform)

    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return db_game


def delete_game(db: Session, game_id: int):
    db_game = get_game_by_id(db=db, game_id=game_id)
    db.delete(db_game)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
