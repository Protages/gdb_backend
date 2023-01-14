from fastapi import Response, status
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from sqlalchemy.sql import Update

from src.models import models
from src.schemas.user_schemas import UserCreate, UserUpdate
from src.core.security import create_hashing_password
from src.crud import role_crud
from src.api_v1.validators import uniqe_validator


def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: UserCreate) -> models.User:
    uniqe_validator(model=models.User, obj=user, field_name='username', db=db)
    uniqe_validator(model=models.User, obj=user, field_name='email', db=db)

    hashed_password = create_hashing_password(user.password)
    roles_id = user.roles
    db_user = models.User(
        **jsonable_encoder(user, exclude={'password', 'roles'}),
        hashed_password=hashed_password
    )
    for role_id in roles_id:
        role = role_crud.get_role_by_id(db=db, role_id=role_id)
        db_user.roles.append(role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, update_user: UserUpdate) -> models.User:
    uniqe_validator(model=models.User, obj=update_user, field_name='username', db=db)
    uniqe_validator(model=models.User, obj=update_user, field_name='email', db=db)

    db_user = get_user_by_id(db=db, user_id=user_id)
    roles_id = update_user.roles

    update_data = jsonable_encoder(
        update_user, exclude={'password', 'roles'}, exclude_unset=True
    )

    new_password = update_user.password
    if new_password:
        new_hashed_password = create_hashing_password(new_password)
        update_data.update({'hashed_password': new_hashed_password})

    for field in jsonable_encoder(db_user):
        if field in update_data:
            setattr(db_user, field, update_data[field])

    if roles_id:
        db_user.roles.clear()
        for role_id in roles_id:
            role = role_crud.get_role_by_id(db=db, role_id=role_id)
            db_user.roles.append(role)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

    # res = db.execute(
    #     Update(models.User)
    #     .where(models.User.id == user_id)
    #     .values(**update_data)
    # )


def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db=db, user_id=user_id)
    db.delete(db_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
