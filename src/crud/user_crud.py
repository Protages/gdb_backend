from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.models import models
from src.schemas.user_schemas import UserCreate, UserUpdate
from src.core.security import create_hashing_password


def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: UserCreate) -> models.User:
    hashed_password = create_hashing_password(user.password)
    db_user = models.User(
        **user.dict(exclude={'password'}), hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, update_user: UserUpdate) -> models.User:
    update_data = update_user.dict(exclude={'password'}, exclude_unset=True)
    new_password = update_user.password
    if new_password:
        new_hashed_password = create_hashing_password(new_password)
        update_data.update({'hashed_password': new_hashed_password})
    res = db.execute(
        Update(models.User)
        .where(models.User.id == user_id)
        .values(**update_data)
    )
    db.commit()
    db_user = get_user_by_id(db=db, user_id=user_id)
    return db_user