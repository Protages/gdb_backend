## Запуск приожения

```
git clone https://github.com/Protages/gdb_backend
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```