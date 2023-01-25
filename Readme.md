# Game DataBase

Backend приложение для сайта по играм (аналог Metacritic).

## Стэк
- FastAPI
- SQLAlchemy
- Alembic
- python-jose
- passlib
- Авторизация на JWT token

## Запуск приложения

```
git clone https://github.com/Protages/gdb_backend
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## О приложении
Можно зарегестрироваться и начать ставить оценки интересющим играм. При желании можно написать рецензию на игру. Пользователь может создавать собственные категории и помещать в них конкретные игры (напр. категории 'Прошел' или 'Буду проходить').
