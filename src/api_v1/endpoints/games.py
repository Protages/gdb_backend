from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.models import models
from src.schemas.game_schemas import Game, GameCreate, GameUpdate
from src.schemas.image_schemas import Image
from src.crud import game_crud
from src.api_v1.depends import get_db, oauth2_scheme, Pagination
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
    return db_game


@router.get('/game/all/', response_model=list[Game])
async def read_all_games(
        paginator: Pagination = Depends(), db: Session = Depends(get_db)
    ):
    db_games = game_crud.get_all_games(db=db, size=paginator.size, page=paginator.page)
    return db_games


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


@router.get(
    '/game/{game_id}/main_img', 
    response_class=FileResponse, 
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the game main image",
        }
    })
async def get_game_main_image(game_id: int, db: Session = Depends(get_db)):
    img_path = game_crud.get_game_main_image_path(db=db, game_id=game_id)
    return FileResponse(img_path, media_type="image/png")


@router.post('/game/{game_id}/main_img', status_code=status.HTTP_204_NO_CONTENT)
async def upload_game_main_image(
        game_id: int, image: UploadFile, db: Session = Depends(get_db)
    ):
    response = game_crud.upload_game_main_image(db=db, game_id=game_id, image=image)
    return response


@router.get(
    '/game/{game_id}/images', 
    response_model=list[bytes], 
    response_description="Returns an array of images in base64 format"
)
async def get_game_images_in_base64(game_id: int, db: Session = Depends(get_db)):
    images_base64 = game_crud.get_game_images_base64(db=db, game_id=game_id)
    return images_base64


@router.post('/game/{game_id}/images', status_code=status.HTTP_204_NO_CONTENT)
async def upload_game_images(
        game_id: int, images: list[UploadFile], db: Session = Depends(get_db)
    ):
    response = game_crud.upload_game_images(db=db, game_id=game_id, images=images)
    return response
