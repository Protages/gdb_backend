from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.db.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Pagination:
    def __init__(self, size: int = 50, page: int = 1):
        if size < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The pagination size parameter must be >= 0'
            )
        elif page < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The pagination page parameter must be >= 0'
            )
        self.size = size
        self.page = page
