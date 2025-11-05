import logging
import logging.handlers
import os
from dotenv import load_dotenv


load_dotenv()
LOGLEVEL = os.getenv("LOGLEVEL", "INFO").upper()
numeric_level = getattr(logging, LOGLEVEL, logging.INFO)

# Создаём корневой логгер
logger = logging.getLogger()
logger.setLevel(numeric_level)

formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Консольный хендлер
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Файловый хендлер с ротацией (файлы до 5Мб, хранит 3 резервные)
file_handler = logging.handlers.RotatingFileHandler(
    '/app/logs/app.log', maxBytes=5*1024*1024, backupCount=3, encoding='utf-8'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_logger(name: str):
    return logging.getLogger(name)
