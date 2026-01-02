# ToDo API

Учебный REST API на **FastAPI** для управления задачами личного пользования (to-do list).

Проект создан для обучения и закрепления практик backend-разработки:
- построение REST API,
- работа с БД через SQLAlchemy и Alembic,
- разделение архитектуры на слои,
- тестирование (Pytest),
- контейнеризация (Docker),
- асинхронная обработка фоновых задач через Kafka.


---

## Архитектура проекта

Проект построен по слоистой архитектуре:

    API (FastAPI routers)
    → Services (бизнес-логика)
    → Repository (доступ к данным)
    → DB (ORM-модели, сессии)

### Кратко по слоям

- **api/** — HTTP-слой: роуты FastAPI, DTO, зависимости, обработка исключений на уровне API
- **services/** — бизнес-логика приложения
- **repository/** — работа с БД, изоляция SQLAlchemy
- **models/** — ORM-модели
- **schemas/** — Pydantic-схемы для валидации и сериализации
- **db/** — инициализация БД, engine, session
- **services/producer.py / consumer.py** — минимальная интеграция Kafka

---

## Kafka (минимальная интеграция)

Kafka используется **в учебных целях** и реализована в минимальном объёме:

- при регистрации пользователя создаётся событие;
- событие отправляется в Kafka;
- consumer получает сообщение и выполняет действие (например, отправка email-уведомления).

---

## Конфигурация и окружения

Для настройки приложения используются переменные окружения.

В проекте присутствуют:
- `.env.example` — пример всех необходимых переменных
- `.env` / `.envLOCAL` — локальные конфиги для тестирования и отладки локально (не хранятся в репозитории)
- `settings.py` — централизованная загрузка и валидация конфигурации

Разделение `dev / prod` реализовано на уровне env-файлов и Docker-окружения.

---

## Запуск через Docker (рекомендуется)

Убедитесь, что Docker и Docker Compose установлены.

### Сборка и запуск

    docker compose up --build

После запуска:
- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

### Применение миграций

    alembic upgrade head

### Остановка контейнеров

    docker compose down

---

## Запуск локально (через Poetry)

### Установка зависимостей

    poetry install

### Применение миграций

    poetry run alembic upgrade head

### Запуск приложения

    poetry run uvicorn main:app --reload

Приложение будет доступно по адресу:
http://127.0.0.1:8000  
http://127.0.0.1:8000/docs

⚠️ Для полноценной работы потребуется отдельно запущенные:
- PostgreSQL
- Kafka
- Kafka consumer

Поэтому для разработки рекомендуется Docker.

---

## Тесты

    poetry run pytest

---

## Используемые технологии

- **Python 3.11**
- **FastAPI**
- **SQLAlchemy + Alembic**
- **PostgreSQL**
- **Kafka** (producer / consumer, учебная интеграция)
- **Pytest**
- **Poetry**
- **Docker / Docker Compose**

---

## Структура проекта

    ├─ alembic/                  # миграции БД
    ├─ api/                      # слой API FastAPI
    │   ├─ endpoints/
    │   ├─ dependencies.py
    │   ├─ dto.py
    │   └─ router.py
    │
    ├─ db/                       # инициализация БД
    │   ├─ Base.py
    │   ├─ init_db.py
    │   └─ session.py
    │
    ├─ logger/                   # логирование
    ├─ models/                   # ORM-модели
    ├─ repository/               # слой доступа к данным
    ├─ schemas/                  # Pydantic-схемы
    ├─ services/                 # бизнес-логика + Kafka
    │   ├─ producer.py
    │   └─ consumer.py
    │
    ├─ tests/                    # pytest-тесты
    ├─ .env.example
    ├─ docker-compose.yml
    ├─ Dockerfile
    ├─ main.py
    ├─ settings.py
    └─ README.md

---
