# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем Poetry
RUN pip install poetry

# Создаём директорию приложения
WORKDIR /app

# Копируем файлы Poetry и устанавливаем зависимости
COPY pyproject.toml poetry.lock* ./

# Настраиваем Poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

# Копируем остальной код проекта
COPY . .

# Экспонируем порт (FastAPI обычно слушает 8000)
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


