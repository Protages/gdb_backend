from pathlib import Path

from sqlalchemy.orm import Session

from src.models import models
from src.core.security import CustomTransaction


def remove_old_game_main_image(db_game: models.Game, image_path: str) -> None:
    '''Delete old main image from static'''
    for f in Path(image_path).glob(f'{db_game.main_img_name_prefix}*'):
        if f.is_file():
            f.unlink()


def remove_all_old_game_images(
    db: Session, db_game: models.Game, image_path: str
) -> None:
    '''Delete all old images from database and static'''
    db_images: list[models.Image] = db_game.images

    with CustomTransaction(db=db):
        [db.delete(db_image) for db_image in db_images]
        db.commit()

        for f in Path(image_path).glob(f'{db_game.img_name_prefix}*'):
            if f.is_file():
                f.unlink()
