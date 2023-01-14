from fastapi import Response, status

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.schemas.comment_schemas import CommentCreate, CommentUpdate
from src.models import models


def get_comment_by_id(db: Session, comment_id: int) -> models.Comment:
    db_comment = db.query(models.Comment).\
        filter(models.Comment.id == comment_id).first()
    return db_comment


def create_comment(db: Session, comment: CommentCreate) -> models.Comment:
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update_comment(
        db: Session, comment_id: int, comment: CommentUpdate
    ) -> models.Comment:
    res = db.execute(
        Update(models.Comment)
        .where(models.Comment.id == comment_id)
        .values(**comment.dict(exclude_unset=True))
    )
    db.commit()
    db_comment = get_comment_by_id(db=db, comment_id=comment_id)
    return db_comment


def delete_comment(db: Session, comment_id: int):
    db_comment = get_comment_by_id(db=db, comment_id=comment_id)
    db.delete(db_comment)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
