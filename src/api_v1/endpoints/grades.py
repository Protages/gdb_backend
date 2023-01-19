from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.models import models
from src.schemas.grade_schemas import Grade, GradeCreate, GradeUpdate
from src.crud import grade_crud
from src.api_v1.depends import get_db, oauth2_scheme, Pagination
from src.core import config
from src.core.security import (
    authenticate_user, 
    authenticate_user_by_token, 
    create_access_token
)

router = APIRouter(tags=['Grades'])


@router.get('/grade/{grade_id}', response_model=Grade)
async def read_grade_by_id(grade_id: int, db: Session = Depends(get_db)):
    db_grade = grade_crud.get_grade_by_id(db=db, grade_id=grade_id)
    return db_grade


@router.get('/grade/all/', response_model=list[Grade])
async def read_all_grades(
        paginator: Pagination = Depends(), db: Session = Depends(get_db)
    ):
    db_grades = grade_crud.get_all_grades(
        db=db, size=paginator.size, page=paginator.page
    )
    return db_grades


@router.post('/grade', response_model=Grade)
async def create_grade(grade: GradeCreate, db: Session = Depends(get_db)):
    db_grade = grade_crud.create_grade(db=db, grade=grade)
    return db_grade


@router.put('/grade/{grade_id}', response_model=Grade)
async def update_grade(grade_id: int, grade: GradeUpdate, db: Session = Depends(get_db)):
    db_grade = grade_crud.update_grade(db=db, grade_id=grade_id, grade=grade)
    return db_grade


@router.delete('/grade/{grade_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    response = grade_crud.delete_grade(db=db, grade_id=grade_id)
    return response
