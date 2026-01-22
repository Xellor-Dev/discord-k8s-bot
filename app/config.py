"""
Конфигурация бота - константы и настройки.
"""

# === Discord настройки ===
COMMAND_PREFIX = '!'
BOT_ACTIVITY_NAME = "в Kubernetes GKE"

# === Метрики ===
MAX_LATENCY_HISTORY = 100  # Храним последние 100 значений пинга

# === Логирование ===
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
