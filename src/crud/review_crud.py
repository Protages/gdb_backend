from fastapi import Response, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.schemas.review_schemas import ReviewCreate, ReviewUpdate
from src.api_v1.exceptions import ObjectDoesNotExistException
from src.crud.queries import pagination_query
from src.crud import user_crud, game_crud
from src.models import models


def get_review_by_id(db: Session, review_id: int) -> models.Review:
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not db_review:
        raise ObjectDoesNotExistException(obj_name='review')
    return db_review


def get_all_reviews(db: Session, size: int, page: int) -> list[models.Review]:
    db_reviews = pagination_query(model=models.Review, size=size, page=page, db=db)
    return db_reviews


def create_review(db: Session, review: ReviewCreate) -> models.Review:
    author = user_crud.get_user_by_id(db=db, user_id=review.author)
    game = game_crud.get_game_by_id(db=db, game_id=review.game)
    create_data = jsonable_encoder(review, exclude={'author', 'game'})
    db_review = models.Review(**create_data)
    db_review.author = author
    db_review.game = game

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review


def update_review(db: Session, review_id: int, review: ReviewUpdate) -> models.Review:
    db_review = get_review_by_id(db=db, review_id=review_id)
    update_data = jsonable_encoder(review, exclude_unset=True)

    for field in jsonable_encoder(db_review):
        if field in update_data:
            setattr(db_review, field, update_data[field])

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review


def delete_review(db: Session, review_id: int):
    db_review = get_review_by_id(db=db, review_id=review_id)
    db.delete(db_review)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
