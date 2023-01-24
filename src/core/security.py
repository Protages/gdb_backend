from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.models import models
from src.crud import user_crud
from src.core import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def create_hashing_password(plain_password: str) -> str:
    '''Хеширует полученный "сырой" пароль'''
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''Проверяет соответствует ли "сырой" пароль захешированному паролю'''
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str) -> models.User | bool:
    '''Проверят есть ли пользователь с таким username и password и возвращает его'''
    db_user = user_crud.get_user_by_username(db, username)
    if not db_user:
        return False
    if not verify_password(password, db_user.hashed_password):
        return False
    return db_user


def authenticate_user_by_token(db: Session, token: str) -> models.User | HTTPException:
    '''Проверят валиден ли токен и возвращает соотв юзера'''
    try:
        payload = jwt.decode(
            token=token, key=config.SECRET_KEY, algorithms=config.ALGORITHM
        )
        username: str = payload.get('sub')
        expire: int = payload.get('exp')
    except JWTError:
        # return False
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not (username and expire):
        # return False
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT token has incomplete payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = user_crud.get_user_by_username(db, username)
    return db_user


def create_access_token(db: Session, subject: str, expires_delta: timedelta | None = None) -> str:
    '''Создает jwt-token на основе переданного subject и expires_delta'''
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(
        claims=to_encode, key=config.SECRET_KEY, algorithm=config.ALGORITHM
    )
    return encoded_jwt
