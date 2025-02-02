"""
    Модуль инициализирует logger для записи логов серверных ошибок.
"""

import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    "log.txt",
    maxBytes=1024 * 1024 * 5,
    backupCount=5,
    encoding="utf-8"
)

file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s"
    )
)

logger.addHandler(file_handler)

__all__ = [
    'logger'
]
