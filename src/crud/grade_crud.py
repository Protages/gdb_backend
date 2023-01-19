from fastapi import Response, status
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.schemas.grade_schemas import GradeCreate, GradeUpdate
from src.api_v1.exceptions import ObjectDoesNotExistException
from src.api_v1.validators import unique_together_validator
from src.crud import user_crud, game_crud
from src.crud.queries import pagination_query
from src.models import models


def get_grade_by_id(db: Session, grade_id: int) -> models.Grade:
    db_grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not db_grade:
        raise ObjectDoesNotExistException(obj_name='grade')
    return db_grade


def get_all_grades(db: Session, size: int, page: int) -> list[models.Grade]:
    db_grades = pagination_query(model=models.Grade, size=size, page=page, db=db)
    return db_grades


def create_grade(db: Session, grade: GradeCreate) -> models.Grade:
    unique_together_validator(
        model=models.Grade,
        obj=grade,
        first_field_name='user_id',
        second_field_name='game_id',
        db=db,
        field_names_with_id=True
    )
    
    user_id = grade.user
    game_id = grade.game
    user = user_crud.get_user_by_id(db=db, user_id=user_id)
    game = game_crud.get_game_by_id(db=db, game_id=game_id)
    create_data = jsonable_encoder(grade, exclude={'user', 'game'})
    
    db_grade = models.Grade(**create_data)
    db_grade.user = user
    db_grade.game = game

    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)

    return db_grade


def update_grade(db: Session, grade_id: int, grade: GradeUpdate) -> models.Grade:
    res = db.execute(
        Update(models.Grade)
        .where(models.Grade.id == grade_id)
        .values(**grade.dict(exclude_unset=True))
    )
    db.commit()
    db_grade = get_grade_by_id(db=db, grade_id=grade_id)
    return db_grade


def delete_grade(db: Session, grade_id: int):
    db_grade = get_grade_by_id(db=db, grade_id=grade_id)
    db.delete(db_grade)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
