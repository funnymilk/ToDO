import logging
import logging.handlers
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

LOGLEVEL = os.getenv("LOGLEVEL", "INFO").upper()
numeric_level = getattr(logging, LOGLEVEL, logging.INFO)

# флаги окружения
TESTING = os.getenv("TESTING") == "1"
LOG_TO_FILE = os.getenv("LOG_TO_FILE", "1") == "1"  # выключить файловый логгер без кода


logger = logging.getLogger()
if not logger.handlers:
    logger.setLevel(numeric_level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # консоль всегда есть
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # файловый — только если НЕ тесты и разрешено флагом
    if not TESTING and LOG_TO_FILE:
        # кроссплатформенный путь + автосоздание каталога
        log_path = Path(os.getenv("LOG_FILE", "logs/app.log")).expanduser().resolve()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                log_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except OSError:
            # если вдруг нет прав/пути — не падаем, а логируем в консоль
            logger.warning("File logging disabled: cannot open %s", log_path)

def get_logger(name: str):
    return logging.getLogger(name)
