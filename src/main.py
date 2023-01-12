from fastapi import FastAPI, Depends

from src.api_v1.api import api_v1_router
from src.api_v1.depends import get_db
from src.db.database import Base, SessionLocal, engine
from src.db.init_db import init_db

# Base.metadata.create_all(bind=engine)
init_db(db=SessionLocal())

app = FastAPI(
    # openapi_url='/api/v1/openapi.json', 
    # docs_url='/api/v1/docs', 
    redoc_url=None,
    title='GDB App'
)
app.include_router(api_v1_router)


@app.get('/')
async def root():
    return {'msg': 'This is root path!'}

