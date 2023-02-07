from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.models import models
from src.schemas.user_schemas import User, UserCreate, UserUpdate, UserAndToken
from src.crud import user_crud
from src.api_v1.depends import get_db, oauth2_scheme, Pagination
from src.core.celery.tasks import send_email_confirm_notification
from src.core.config import settings
from src.core.security import (
    authenticate_user, 
    authenticate_user_by_token, 
    create_access_token
)

router = APIRouter(tags=['Users'])


@router.get('/user/me', response_model=User)
async def read_current_user(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ):
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


@router.get('/user/verification_email/{verification_code}')
async def verification_email(verification_code: str, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_verification_code(
        db=db, verification_code=verification_code
    )
    if not db_user.is_email_confirmed:
        db_user.is_email_confirmed = True
        db.add(db_user)
        db.commit()
    
    return {'Email was successfully verified'}


@router.post(
    '/user', 
    response_model=UserAndToken, 
    status_code=status.HTTP_201_CREATED, 
    description='''
    Valid username must be:
    1. Username is 4-32 characters long
    2. No _,- or . at the beginning and end
    3. No __ or . or . or .. or .- or _- inside
    Valid password must be:
    1. At least 6 characters
    2. Allowed: A-Z, a-z, 0-9, @#$%^&+=
    3. At least one letter
    '''
)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user, verification_code = user_crud.create_user(db, user)
    access_token = create_access_token(subject=user.username)
    response = {
        'user': db_user,
        'token': {'access_token': access_token, 'token_type': settings.TOKEN_TYPE}
    }

    if not settings.TESTS_RUNNING:
        verification_url = f'http://127.0.0.1:8000/api/v1/user/verification_email/{verification_code}'
        try:
            send_email_confirm_notification.delay(
                db_user.email, db_user.username, verification_url
            )
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail='Celery is not working'
            )

    return response


@router.put('/user/{user_id}', response_model=User)
async def update_user(user_id, update_user: UserUpdate, db: Session = Depends(get_db)):
    db_user = user_crud.update_user(db=db, user_id=user_id, update_user=update_user)
    return db_user


@router.delete('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    response = user_crud.delete_user(db=db, user_id=user_id)
    return response
