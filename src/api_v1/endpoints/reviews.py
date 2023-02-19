
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.schemas.review_schemas import Review, ReviewCreate, ReviewUpdate
from src.crud import review_crud
from src.api_v1.depends import get_db, Pagination


router = APIRouter(prefix='/review', tags=['Reviews'])


@router.get('/{review_id}', response_model=Review)
async def read_review_by_id(review_id: int, db: Session = Depends(get_db)):
    db_review = review_crud.get_review_by_id(db=db, review_id=review_id)
    return db_review


@router.get('/', response_model=list[Review])
async def read_all_review(
    paginator: Pagination = Depends(), db: Session = Depends(get_db)
):
    db_reviews = review_crud.get_all_reviews(
        db=db, size=paginator.size, page=paginator.page
    )
    return db_reviews


@router.post('/', response_model=Review, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = review_crud.create_review(db=db, review=review)
    return db_review


@router.put('/{review_id}', response_model=Review)
async def update_review(
    review_id: int, review: ReviewUpdate, db: Session = Depends(get_db)
):
    db_review = review_crud.update_review(db=db, review_id=review_id, review=review)
    return db_review


@router.delete('/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    response = review_crud.delete_review(db=db, review_id=review_id)
    return response
