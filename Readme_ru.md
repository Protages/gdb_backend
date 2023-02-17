# Game DataBase

Backend приложение для игрового проекта.

## Стек
- FastAPI
- SQLAlchemy
- Alembic
- Celery
- Redis
- python-jose
- passlib
- Авторизация на JWT token

## Запуск приложения
```properties
git clone https://github.com/Protages/gdb_backend
```

Создаем `venv` и активируем его
```properties
python -m venv env
.\env\Scripts\activate
```

Устанавливаем `зависимости` и запускаем `uvicorn сервер`
```properties
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Запуск `Redis` в docker
```properties
docker run -p 127.0.0.1:16379:6379 --name my-redis -d redis
```

Запуск Celery на `Unix` 
```properties
celery -A src.core.celery.celery worker --loglevel=INFO
```

Или запуск Celery на `Windows` 
```properties
celery -A src.core.celery.celery worker --loglevel=INFO --pool=solo
```

## Тестирование
Запуск интеграционных тестов
```properties
pytest ./tests/endpoints/ --verbosity=2 --order-group-scope=module
```

Запуск тестов миграций
```properties
pytest ./tests/migrations/ --verbosity 2
```

## О приложении
Можно зарегестрироваться и начать ставить оценки интересющим играм. При желании можно написать рецензию на игру. Пользователь может создавать собственные категории и помещать в них конкретные игры (напр. категории 'Прошел' или 'Буду проходить').
