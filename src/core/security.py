import random
import hashlib
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.models import models
from src.crud import user_crud
from src.core.config import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CustomTransaction:
    '''Context Manager that implements transactions in the database'''

    def __init__(self, db: Session) -> None:
        self.db = db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            self.db.rollback()
            return False
        return True


def create_hashing_password(plain_password: str) -> str:
    '''Hashes the received raw password'''
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''Checks whether raw password matches hashed password'''
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str) -> models.User | bool:
    '''Check if there is a user with such username and password and returns it'''
    db_user = user_crud.get_user_by_username(db, username)
    if not db_user:
        return False
    if not verify_password(password, db_user.hashed_password):
        return False
    return db_user


def authenticate_user_by_token(db: Session, token: str) -> models.User | HTTPException:
    '''Checks whether token is valid and returns user's corresponding'''
    try:
        payload = jwt.decode(
            token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        username: str = payload.get('sub')
        expire: int = payload.get('exp')
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='JWT token has expired',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    if not (username and expire):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='JWT token has incomplete payload',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    db_user = user_crud.get_user_by_username(db, username)
    return db_user


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    '''Creates a jwt token based on passed subject and expires_delta'''
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + \
                 timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {'exp': expire, 'sub': subject}
    encoded_jwt = jwt.encode(
        claims=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_verification_email_code(lenght: int = 10) -> str:
    '''Creates a unique encrypted email verification code'''

    token = random.randbytes(lenght)
    hashedCode = hashlib.sha256()
    hashedCode.update(token)
    verification_code = hashedCode.hexdigest()

    return verification_code
