"""
Настройка логирования для бота.
Заменяет простой print() на профессиональное логирование.
"""

import logging
import sys
from config import LOG_LEVEL, LOG_FORMAT, LOG_DATE_FORMAT


def setup_logger(name: str = "discord_bot") -> logging.Logger:
    """
    Создает и настраивает логгер.
    
    Args:
        name: Имя логгера (по умолчанию "discord_bot")
    
    Returns:
        Настроенный экземпляр logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Проверяем, не добавлены ли уже обработчики (чтобы не дублировать)
    if not logger.handlers:
        # Создаем обработчик для вывода в консоль
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(LOG_LEVEL)
        
        # Создаем форматтер
        formatter = logging.Formatter(
            fmt=LOG_FORMAT,
            datefmt=LOG_DATE_FORMAT
        )
        handler.setFormatter(formatter)
        
        # Добавляем обработчик к логгеру
        logger.addHandler(handler)
    
    return logger
