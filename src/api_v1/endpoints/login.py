from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.schemas.user_schemas import UserAndToken
from src.api_v1.depends import get_db
from src.core.config import settings
from src.core.security import (
    authenticate_user,
    create_access_token
)

router = APIRouter(tags=['Users', 'Auth'])


@router.post('/token', response_model=UserAndToken)
async def login(
    login_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = authenticate_user(
        db=db, username=login_form.username, password=login_form.password
    )
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": settings.TOKEN_TYPE},
        )
    expire_time_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=db_user.username, expires_delta=expire_time_delta
    )
    response = {
        'user': db_user,
        'token': {'access_token': access_token, 'token_type': settings.TOKEN_TYPE}
    }
    return response
