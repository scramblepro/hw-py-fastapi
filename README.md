
FastAPI-сервис объявлений
Простой API для создания, редактирования, удаления и получения объявлений с авторизацией пользователей и ролями.

Установка и запуск:

git clone https://github.com/yourusername/your-repo.git
cd your-repo
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
cp .env.example .env

Переменные окружения (.env):
Создайте файл .env по шаблону .env.example

Запуск приложения:

uvicorn app.main:app --reload

Аутентификация:

Используется JWT. Для запросов, требующих авторизации, нужно передавать токен:

Authorization: Bearer <ваш_токен>

Примеры запросов:
Файл requests.http содержит готовые запросы для тестирования (можно открыть в PyCharm или VS Code с REST Client).