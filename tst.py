from sqlalchemy import text
from db.session import engine

print("Проверяю соединение...")

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("✅ Подключение успешно!")
        print("Версия Postgres:", result.scalar())
except Exception as e:
    print("❌ Ошибка при подключении:")
    print(e)
