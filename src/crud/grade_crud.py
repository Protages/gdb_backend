from fastapi import Response, status

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.schemas.grade_schemas import GradeCreate, GradeUpdate
from src.models import models


def get_grade_by_id(db: Session, grade_id: int) -> models.Grade:
    db_grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    return db_grade


def create_grade(db: Session, grade: GradeCreate) -> models.Grade:
    db_grade = models.Grade(**grade.dict())
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
