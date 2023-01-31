import os
import pytest

from sqlalchemy import create_engine

from tests.utils import alembic_config_from_url, tmp_database, DEFAULT_SQLITE_URL


@pytest.fixture(scope='session')
def pg_url():
    """
    Provides base SQLite URL for creating temporary databases.
    """
    return DEFAULT_SQLITE_URL
    
    # For PostgreSQL
    # return URL(os.getenv('CI_STAFF_PG_URL', DEFAULT_PG_URL))


@pytest.fixture
def sqlite(pg_url):
    """
    Creates empty temporary database.
    """
    with tmp_database(pg_url, 'pytest') as tmp_url:
        yield tmp_url


@pytest.fixture()
def sqlite_engine(sqlite):
    """
    SQLAlchemy engine, bound to temporary database.
    """
    engine = create_engine(sqlite, echo=True)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture()
def alembic_config(sqlite):
    """
    Alembic configuration object, bound to temporary database.
    """
    return alembic_config_from_url(sqlite)
