# ToDo API

Небольшое REST API на **FastAPI** для управления задачами (to-do list).  
Проект создан для обучения и демонстрации навыков работы с FastAPI, SQLAlchemy, тестами на Pytest и попробовать другие важные сервисы типа Kafka.

---

## Запуск через Docker

Убедитесь, что Docker установлен.

### 1. Сборка и запуск
```powershell
docker compose up --build
```
После сборки приложение будет доступно по адресу: http://127.0.0.1:8000  
Swagger UI: http://127.0.0.1:8000/docs

### 2. Применение миграций внутри контейнера
Миграции выполняются с хоста — Alembic использует переменные окружения из `.env`:

```powershell
alembic upgrade head
```

### 3. Остановка контейнеров
```powershell
docker compose down
```
---

## Запуск (локально, через Poetry)

### 1. Установка зависимостей
```powershell
poetry install
```

### 2. Применение миграций
```powershell
poetry run alembic upgrade head
```

### 3. Запуск приложения
```powershell
poetry run uvicorn main:app --reload
```
Приложение будет доступно по адресу: http://127.0.0.1:8000  
Swagger UI: http://127.0.0.1:8000/docs
Что-бы приложение работало полноценно, надо будет отдельно запускать PostgreSQL, Kafka, да и comsumer, так что рекомендую всё таки Docker.

---
---

## Тесты
```powershell
poetry run pytest
```
---

## Используемые технологии
- **Python 3.11**
- **FastAPI**
- **SQLAlchemy + Alembic**
- **Pytest**
- **Poetry**
- **Docker** (проект можно адаптировать под контейнеризацию)
- **Kafka** (используется локально для отправки писем при создании пользователя)

---

## Структура проекта

```
├─ alembic/                  # миграции БД (env.py, versions/*)
│   ├─ versions/             # файлы версий миграций
│   ├─ env.py
│   └─ README
│
├─ api/                      # слой API FastAPI
│   ├─ endpoints/            # роуты (users, tasks)
│   │   ├─ task_endpoints.py
│   │   └─ user_endpoints.py
│   ├─ dependencies.py       # зависимости / DI
│   ├─ dto.py                # DTO-сущности API
│   ├─ exceptions_handlers.py
│   └─ router.py
│
├─ db/                       # слой базы данных
│   ├─ Base.py               # декларативная база SQLAlchemy
│   ├─ init_db.py            # инициализация БД (при необходимости)
│   └─ session.py            # создание сессии и engine
│
├─ home/                     # домашняя страница / шаблоны (если нужны)
│
├─ logger/                   # логирование
│   └─ logger.py
│
├─ logs/                     # каталог для логов (в .gitignore)
│
├─ models/                   # ORM-модели SQLAlchemy
│   └─ models.py
│
├─ repository/               # слой доступа к данным
│   ├─ repository.py
│   ├─ task_repository.py
│   ├─ user_repository.py
│   └─ *_exceptions.py
│
├─ schemas/                  # Pydantic-схемы (валидация данных)
│   └─ schemas.py
│
├─ services/                 # бизнес-логика
│   ├─ task_service.py
│   ├─ user_service.py
│   ├─ producer.py           # Kafka producer
│   ├─ consumer.py           # Kafka consumer
│   └─ *_exceptions.py
│
├─ tests/                    # pytest-тесты
│
├─ .env.example              # пример переменных окружения
├─ alembic.ini
├─ docker-compose.yml
├─ Dockerfile
├─ main.py                   # точка входа FastAPI
├─ poetry.lock
├─ pyproject.toml
├─ pytest.ini
├─ settings.py               # конфигурация приложения
└─ README.md
```


---
