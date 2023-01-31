from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.api_v1.api import api_v1_router
from src.db.database import Base, SessionLocal, engine
from src.db.init_db import init_db
from src.api_v1.exceptions import ObjectDoesNotExistException

# Base.metadata.create_all(bind=engine)
# init_db(db=SessionLocal())

origins = [
    'http://localhost:8000',
]

app = FastAPI(
    # openapi_url='/api/v1/openapi.json',
    # docs_url='/api/v1/docs',
    # redoc_url='/api/v1/redocs',
    title='GDB App'
)
app.mount('/src/static', StaticFiles(directory='src/static'), name='static')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
app.include_router(api_v1_router)


@app.get('/')
async def root():
    return {'msg': 'This is root path! To view docs go to http://127.0.0.1:8000/docs/'}


@app.exception_handler(ObjectDoesNotExistException)
async def object_does_not_exist_exception_handler(
        request: Request, exc: ObjectDoesNotExistException
    ):
    return JSONResponse(status_code=exc.status_code, content=exc.content)
