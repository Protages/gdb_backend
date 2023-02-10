import pytest
from typing import Generator, Any

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from src.main import app
from src.db.database import Base
from src.core import config
from src.api_v1 import depends
from tests.utils import tmp_database, DEFAULT_SQLITE_URL


@pytest.fixture(scope='session')
def sqlite() -> Generator[str, None, None]:
    '''Creates a temporary sqlite database, and then closes it'''
    with tmp_database(DEFAULT_SQLITE_URL, 'endpoints') as tmp_url:
        yield tmp_url

    
@pytest.fixture(scope='session')
def sqlite_engine(sqlite: Generator[str, None, None]) -> Generator[Engine, None, None]:
    '''Create sqlite engine'''
    engine = create_engine(sqlite, connect_args={'check_same_thread': False})
    try:
        yield engine
    finally:
        engine.dispose()


def create_all_db_models(engine) -> None:
    '''Creates all linked models'''
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope='session')
def create_sessionmaker(
        sqlite_engine: Generator[Engine, None, None]
    ) -> Generator[sessionmaker, None, None]:
    create_all_db_models(sqlite_engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)
    yield SessionLocal


@pytest.fixture(scope='function')
def get_session(create_sessionmaker: Generator[sessionmaker, None, None]):
    def get_db() -> Generator[Session, None, None]:
        db: Session = create_sessionmaker()
        try:
            yield db
        finally:
            db.close()
    return get_db


@pytest.fixture(scope='function')
def test_client(get_session) -> Generator[TestClient, None, None]:
    '''
    Creates a TestClient and overrides get_in() dependency of temporary database
    '''
    app.dependency_overrides[depends.get_db] = get_session
    client = TestClient(app)
    yield client
