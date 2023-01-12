from fastapi.security import OAuth2PasswordBearer

from src.db.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()
