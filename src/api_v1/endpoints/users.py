from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.models import models
from src.schemas.user_schemas import User, UserCreate, UserUpdate, UserAndToken
from src.crud import user_crud
from src.api_v1.depends import get_db, oauth2_scheme, Pagination
from src.core import config
from src.core.security import (
    authenticate_user, 
    authenticate_user_by_token, 
    create_access_token
)

router = APIRouter(tags=['Users'])


@router.get('/user/me', response_model=User)
async def read_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    db_user = authenticate_user_by_token(db=db, token=token)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db_user


@router.get('/user/{user_id}', response_model=User)
async def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db, user_id)
    return db_user


@router.get('/user/all/', response_model=list[User])
async def read_all_users(
        paginator: Pagination = Depends(), db: Session = Depends(get_db)
    ):
    db_users = user_crud.get_all_users(db=db, size=paginator.size, page=paginator.page)
    return db_users


@router.post('/user', response_model=UserAndToken)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(db, user)
    access_token = create_access_token(db=db, subject=user.username)
    response = {
        'user': db_user,
        'token': {'access_token': access_token, 'token_type': config.TOKEN_TYPE}
    }
    return response


@router.put('/user/{user_id}', response_model=User)
async def update_user(user_id, update_user: UserUpdate, db: Session = Depends(get_db)):
    db_user = user_crud.update_user(db=db, user_id=user_id, update_user=update_user)
    return db_user


@router.delete('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    response = user_crud.delete_user(db=db, user_id=user_id)
    return response
