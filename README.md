# ToDo API

Небольшое REST API на **FastAPI** для управления задачами (to-do list).  
Проект создан для обучения и демонстрации навыков работы с FastAPI, SQLAlchemy, тестами на Pytest и попробовать другие важные сервисы типа Kafka.

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

---

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
app/
 ├─ api/              # эндпоинты и схемы
 ├─ services/         # бизнес-логика
 ├─ repository/       # доступ к БД
 ├─ logger/           # логирование
 └─ main.py           # точка входа
tests/
 └─ ...               # тесты
```

---