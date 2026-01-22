"""
Сбор метрик для команды !ping.
Простой синглтон для отслеживания команд и latency.
"""

from typing import List, Optional
from config import MAX_LATENCY_HISTORY


class MetricsCollector:
    """
    Синглтон для сбора метрик бота.
    Заменяет глобальные переменные из старого кода.
    """
    _instance: Optional['MetricsCollector'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # Метрики команд
        self.commands_executed = 0
        self.api_latency_list: List[int] = []
        
        self._initialized = True
    
    def increment_command_counter(self):
        """Увеличивает счетчик выполненных команд."""
        self.commands_executed += 1
    
    def record_latency(self, latency_ms: int):
        """
        Записывает пинг в историю.
        
        Args:
            latency_ms: Задержка в миллисекундах
        """
        self.api_latency_list.append(latency_ms)
        if len(self.api_latency_list) > MAX_LATENCY_HISTORY:
            self.api_latency_list.pop(0)
    
    def get_average_latency(self) -> int:
        """Возвращает средний пинг."""
        if not self.api_latency_list:
            return 0
        return round(sum(self.api_latency_list) / len(self.api_latency_list))
