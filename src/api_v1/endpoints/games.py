from fastapi import APIRouter, Depends, status, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.schemas.game_schemas import Game, GameCreate, GameUpdate
from src.crud import game_crud
from src.api_v1.depends import get_db, Pagination


router = APIRouter(prefix='/game', tags=['Games'])


@router.get('/{game_id}', response_model=Game)
async def read_game_by_id(game_id: int, db: Session = Depends(get_db)):
    db_game = game_crud.get_game_by_id(db=db, game_id=game_id)
    return db_game


@router.get('/', response_model=list[Game])
async def read_all_games(
    paginator: Pagination = Depends(), db: Session = Depends(get_db)
):
    db_games = game_crud.get_all_games(db=db, size=paginator.size, page=paginator.page)
    return db_games


@router.post('/', response_model=Game, status_code=status.HTTP_201_CREATED)
async def create_game(game: GameCreate, db: Session = Depends(get_db)):
    db_game = game_crud.create_game(db=db, game=game)
    return db_game


@router.put('/{game_id}', response_model=Game)
async def update_game(game_id: int, game: GameUpdate, db: Session = Depends(get_db)):
    db_game = game_crud.update_game(db=db, game_id=game_id, game=game)
    return db_game


@router.delete('/{game_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id: int, db: Session = Depends(get_db)):
    response = game_crud.delete_game(db=db, game_id=game_id)
    return response


@router.get(
    '/{game_id}/main_img',
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


@router.post('/{game_id}/main_img', status_code=status.HTTP_204_NO_CONTENT)
async def upload_game_main_image(
    game_id: int, image: UploadFile, db: Session = Depends(get_db)
):
    response = game_crud.upload_game_main_image(db=db, game_id=game_id, image=image)
    return response


@router.get(
    '/{game_id}/images',
    response_model=list[bytes],
    response_description="Returns an array of images in base64 format"
)
async def get_game_images_in_base64(game_id: int, db: Session = Depends(get_db)):
    images_base64 = game_crud.get_game_images_base64(db=db, game_id=game_id)
    return images_base64


@router.post(
    '/{game_id}/images',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Remove all old game images(!), and upload new images'
)
async def upload_game_images(
    game_id: int, images: list[UploadFile], db: Session = Depends(get_db)
):
    response = game_crud.upload_game_images(db=db, game_id=game_id, images=images)
    return response


@router.patch(
    '/{game_id}/images',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Add new images to game, keeps old images'
)
async def add_images_to_game(
    game_id: int, images: list[UploadFile], db: Session = Depends(get_db)
):
    response = game_crud.upload_game_images(
        db=db, game_id=game_id, images=images, patch=True
    )
    return response
