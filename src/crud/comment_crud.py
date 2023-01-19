from fastapi import Response, status, HTTPException
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.schemas.comment_schemas import CommentCreate, CommentUpdate
from src.api_v1.exceptions import ObjectDoesNotExistException
from src.models import models
from src.crud import game_crud, review_crud, user_crud
from src.crud.queries import pagination_query


def get_comment_by_id(db: Session, comment_id: int) -> models.Comment:
    db_comment = db.query(models.Comment).\
        filter(models.Comment.id == comment_id).first()
    if not db_comment:
        raise ObjectDoesNotExistException(obj_name='comment')
    return db_comment


def get_all_comments(db: Session, size: int, page: int) -> list[models.Comment]:
    db_comments = pagination_query(model=models.Comment, size=size, page=page, db=db)
    return db_comments


def create_comment(db: Session, comment: CommentCreate) -> models.Comment:
    user_id = comment.user
    game_id = comment.game
    review_id = comment.review

    create_data = jsonable_encoder(comment, exclude={'user', 'game', 'review'})
    db_comment = models.Comment(**create_data)
    user = user_crud.get_user_by_id(db=db, user_id=user_id)
    db_comment.user = user

    if game_id and review_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Pass game ID or review ID, not together'
        )
    elif game_id:
        game = game_crud.get_game_by_id(db=db, game_id=game_id)
        db_comment.game = game
    elif review_id:
        review = review_crud.get_review_by_id(db=db, review_id=review_id)
        db_comment.review = review
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Need to pass game ID or review ID'
        )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment


def update_comment(
        db: Session, comment_id: int, comment: CommentUpdate
    ) -> models.Comment:
    db_comment = get_comment_by_id(db=db, comment_id=comment_id)
    update_data = jsonable_encoder(comment, exclude_unset=True)

    for field in jsonable_encoder(db_comment):
        if field in update_data:
            setattr(db_comment, field, update_data[field])

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment


def delete_comment(db: Session, comment_id: int):
    db_comment = get_comment_by_id(db=db, comment_id=comment_id)
    db.delete(db_comment)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
