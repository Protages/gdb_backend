from fastapi.security import OAuth2PasswordBearer

from src.db.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


class Pagination:
    def __init__(self, size: int = 50, page: int = 1):
        self.size = size
        self.page = page
