import base64
import datetime
from pathlib import Path

from fastapi import Response, status, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.schemas.game_schemas import GameCreate, GameUpdate
from src.api_v1.exceptions import ObjectDoesNotExistException
from src.models import models
from src.crud import genre_crud, platform_crud
from src.crud.queries import pagination_query


def get_game_by_id(db: Session, game_id: int) -> models.Game:
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not db_game:
        raise ObjectDoesNotExistException(obj_name='game')
    return db_game


def get_all_games(db: Session, size: int, page: int) -> list[models.Game]:
    db_games = pagination_query(model=models.Game, size=size, page=page, db=db)
    return db_games


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


def get_game_main_image_path(db: Session, game_id: int) -> str:
    db_game = get_game_by_id(db=db, game_id=game_id)
    image_path = db_game.main_image_path
    is_exist = Path(image_path).exists() if image_path else False
    if not is_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Image not exist'
        )
    return image_path


def upload_game_main_image(db: Session, game_id: int, image: UploadFile):
    db_game = get_game_by_id(db=db, game_id=game_id)
    image_path = db_game.create_image_path()
    iamge_name = db_game.create_main_image_name(file_name=image.filename)
    image_url = f'{image_path}/{iamge_name}'

    with open(image_url, 'wb') as out_file:
        content = image.file.read()
        out_file.write(content)
    
    db_game.main_image_path = image_url

    db.add(db_game)
    db.commit()

    return Response(status_code=status.HTTP_200_OK)


def get_game_images_base64(db: Session, game_id: int) -> list[bytes]:
    db_game = get_game_by_id(db=db, game_id=game_id)
    db_images = db_game.images
    images_base64 = []

    for db_image in db_images:
        image_path = db_image.image_path
        is_exist = Path(image_path).exists() if image_path else False
        if not is_exist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Image not exist'
            )
        with open(image_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read())
            images_base64.append(img_base64)

    return images_base64


def upload_game_images(db: Session, game_id: int, images: list[UploadFile]):
    db_game = get_game_by_id(db=db, game_id=game_id)
    image_path = db_game.create_image_path()

    for indx in range(len(images)):
        db_image = models.Image(game_id=db_game.id)
        iamge_name = db_image.create_image_name(
            indx=indx, file_name=images[indx].filename
        )
        image_url = f'{image_path}/{iamge_name}'

        with open(image_url, 'wb') as out_file:
            content = images[indx].file.read()
            out_file.write(content)
        
        db_image.image_path = image_url
        db.add(db_image)

    db.commit()

    return Response(status_code=status.HTTP_200_OK)
