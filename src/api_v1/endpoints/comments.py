from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.schemas.comment_schemas import Comment, CommentCreate, CommentUpdate
from src.crud import comment_crud
from src.api_v1.depends import get_db, Pagination


router = APIRouter(prefix='/comment', tags=['Comments'])


@router.get('/{comment_id}', response_model=Comment)
async def read_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    comment = comment_crud.get_comment_by_id(db=db, comment_id=comment_id)
    return comment


@router.get('/', response_model=list[Comment])
async def read_all_comments(
    paginator: Pagination = Depends(), db: Session = Depends(get_db)
):
    db_comments = comment_crud.get_all_comments(
        db=db, size=paginator.size, page=paginator.page
    )
    return db_comments


@router.post('/', response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    comment = comment_crud.create_comment(db=db, comment=comment)
    return comment


@router.put('/{comment_id}', response_model=Comment)
async def update_comment(
    comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db)
):
    comment = comment_crud.update_comment(db=db, comment_id=comment_id, comment=comment)
    return comment


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    response = comment_crud.delete_comment(db=db, comment_id=comment_id)
    return response
