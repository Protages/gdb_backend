from fastapi import Response, status
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.schemas.category_schemas import CategoryCreate, CategoryUpdate
from src.api_v1.exceptions import ObjectDoesNotExistException
from src.api_v1.validators import unique_together_validator
from src.crud import user_crud, game_crud
from src.crud.queries import pagination_query
from src.models import models


def get_category_by_id(db: Session, category_id: int) -> models.Category:
    db_category = db.query(models.Category)\
        .filter(models.Category.id == category_id).first()
    if not db_category:
        raise ObjectDoesNotExistException(obj_name='category')
    return db_category


def get_all_categories(db: Session, size: int, page: int) -> list[models.Category]:
    db_categories = pagination_query(model=models.Category, size=size, page=page, db=db)
    return db_categories


def get_categories_by_user_id(
        db: Session, size: int, page: int, user_id: int
    ) -> list[models.Category]:
    filter = models.Category.user_id == user_id 
    db_categories = pagination_query(
        model=models.Category, size=size, page=page, filter=filter, db=db
    )
    return db_categories


def create_category(db: Session, category: CategoryCreate) -> models.Category:
    unique_together_validator(
        model=models.Category, 
        obj=category, 
        first_field_name='title', 
        second_field_name='user_id',
        db=db,
        field_names_with_id=True
    )
    user_id = category.user
    games_id = category.games
    user = user_crud.get_user_by_id(db=db, user_id=user_id)

    create_data = jsonable_encoder(category, exclude={'user', 'games'})
    db_category = models.Category(**create_data)
    db_category.user = user

    for game_id in games_id:
        game = game_crud.get_game_by_id(db=db, game_id=game_id)
        db_category.games.append(game)

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


def update_category(
        db: Session, category_id: int, category: CategoryUpdate
    ) -> models.Category:
    db_category = get_category_by_id(db=db, category_id=category_id)
    games_id = category.games
    update_data = jsonable_encoder(category, exclude={'games'}, exclude_unset=True)

    if games_id:
        db_category.games.clear()
        for game_id in games_id:
            game = game_crud.get_game_by_id(db=db, game_id=game_id)
            db_category.games.append(game)

    for field in jsonable_encoder(db_category):
        if field in update_data:
            setattr(db_category, field, update_data[field])

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


def delete_category(db: Session, category_id: int):
    db_category = get_category_by_id(db=db, category_id=category_id)
    db.delete(db_category)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def add_game_to_category(db: Session, catgory_id: int, game_id: int) -> models.Category:
    db_category = get_category_by_id(db=db, category_id=catgory_id)
    game = game_crud.get_game_by_id(db=db, game_id=game_id)
    db_category.games.append(game)

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


def remove_game_from_category(
        db: Session, catgory_id: int, game_id: int
    ) -> models.Category:
    db_category = get_category_by_id(db=db, category_id=catgory_id)
    game = game_crud.get_game_by_id(db=db, game_id=game_id)
    db_category.games.remove(game)

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category
