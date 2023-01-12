from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.models import models
from src.schemas.user_schemas import User, UserCreate, UserUpdate
from src.crud import user_crud
from src.api_v1.depends import get_db, oauth2_scheme
from src.core import config
from src.core.security import (
    authenticate_user, 
    authenticate_user_by_token, 
    create_access_token
)

router = APIRouter(tags=['users'])


@router.get('/users/me', response_model=User)
async def read_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = authenticate_user_by_token(db=db, token=token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.get('/users/{user_id}', response_model=User)
async def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db, user_id)
    return user


@router.post('/users', response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = user_crud.create_user(db, user)
    return user


@router.put('/users/{user_id}', response_model=User)
async def update_user(user_id, update_user: UserUpdate, db: Session = Depends(get_db)):
    user = user_crud.update_user(db=db, user_id=user_id, update_user=update_user)
    return user
