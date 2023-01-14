from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.schemas.token_schemas import Token
from src.api_v1.depends import get_db, oauth2_scheme
from src.core import config
from src.core.security import (
    authenticate_user, 
    authenticate_user_by_token, 
    create_access_token
)

router = APIRouter(tags=['Users', 'Auth'])


@router.post('/token', response_model=Token)
async def login(login_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(
        db=db, username=login_form.username, password=login_form.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expire_time_delta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        db=db, subject=user.username, expires_delta=expire_time_delta
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
