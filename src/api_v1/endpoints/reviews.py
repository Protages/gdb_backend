from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.models import models
from src.schemas.review_schemas import Review, ReviewCreate, ReviewUpdate
from src.crud import review_crud
from src.api_v1.depends import get_db, oauth2_scheme, Pagination
from src.core import config
from src.core.security import (
    authenticate_user, 
    authenticate_user_by_token, 
    create_access_token
)

router = APIRouter(tags=['Reviews'])


@router.get('/review/{review_id}', response_model=Review)
async def read_review_by_id(review_id: int, db: Session = Depends(get_db)):
    db_review = review_crud.get_review_by_id(db=db, review_id=review_id)
    return db_review


@router.get('/review/all/', response_model=list[Review])
async def read_all_review(
        paginator: Pagination = Depends(), db: Session = Depends(get_db)
    ):
    db_reviews = review_crud.get_all_reviews(
        db=db, size=paginator.size, page=paginator.page
    )
    return db_reviews


@router.post('/review', response_model=Review)
async def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = review_crud.create_review(db=db, review=review)
    return db_review


@router.put('/review/{review_id}', response_model=Review)
async def update_review(
        review_id: int, review: ReviewUpdate, db: Session = Depends(get_db)
    ):
    db_review = review_crud.update_review(db=db, review_id=review_id, review=review)
    return db_review


@router.delete('/review/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    response = review_crud.delete_review(db=db, review_id=review_id)
    return response
