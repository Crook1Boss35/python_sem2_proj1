LLM (FastAPI)
Описание проекта: данный проект представляет собой приложение на FastAPI с поддержкой:
JWT-аутентификации
работы с базой данных SQLite
хранения истории диалога
интеграции с LLM через OpenRouter

Особенности:

бизнес-логика вынесена в usecases
работа с БД — через repositories
dependency injection через Depends
API слой не содержит бизнес-логики

Виртуальное окружение
uv venv
source .venv/bin/activate

Установка зависимостей
uv pip install -r requirements.txt

.env
JWT_SECRET=change_me_super_secret
OPENROUTER_API_KEY=your_api_key
OPENROUTER_MODEL=stepfun/step-3.5-flash

Запуск
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

Swagger
http://127.0.0.1:8000/docs

## Регистрация

![register](./screenshots/register.png)

## Логин

![login](./screenshots/login.png)

## Авторизация

![authorize](./screenshots/authorize.png)

## Chat

![chat](./screenshots/chat.png)

## History

![history](./screenshots/history.png)

## Delete

![delete](./screenshots/delete.png)

## Empty history

![empty](./screenshots/empty.png)

