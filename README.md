# FastAPI Homework Project

Простой API-сервис на FastAPI с JWT-аутентификацией, CRUD и разделением прав пользователя.

---

## Быстрый старт

1. Клонируем репозиторий:
   git clone https://github.com/scramblepro/hw-py-fastapi.git
   cd hw-py-fastapi
   
Создаем виртуальное окружение и устанавливаем зависимости:
python3 -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
pip install -r requirements.txt

Создаем .env файл в корне:
DATABASE_URL=sqlite:///./test.db      # или PostgreSQL: postgresql://user:pass@host/dbname
SECRET_KEY=your_jwt_secret_key

Запускаем миграции (если используются):
alembic upgrade head

Запускаем сервер:
uvicorn app.main:app --reload

Открываем браузер:
Swagger UI: http://127.0.0.1:8000/docs
ReDoc (документация): http://127.0.0.1:8000/redoc

