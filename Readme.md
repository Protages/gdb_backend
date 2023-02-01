# Game DataBase

Backend application for a game project.

## Stack
- FastAPI
- SQLAlchemy
- Alembic
- Celery
- Redis
- python-jose
- passlib
- Authorization on JWT token

## Installation
```properties
git clone https://github.com/Protages/gdb_backend
```

Create `venv` and activate it
```properties
python -m venv env
.\env\Scripts\activate
```

Install the `dependencies` and launch the `unicorn server`
```properties
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Run `Redis` on docker
```properties
docker run -p 127.0.0.1:16379:6379 --name my-redis -d redis
```

Run Celery on `Unix` 
```properties
celery -A src.core.celery.celery worker --loglevel=INFO
```

Or run Celery on `Windows` 
```properties
celery -A src.core.celery.celery worker --loglevel=INFO --pool=solo
```

## About
You can register and start rating interesting games. If desired, you can write a review of the game. The user can create their own categories and put specific games in them (e.g. the categories 'Passed' or 'Will pass').
