"""
Модуль для получения Kubernetes метаданных из переменных окружения.
Использует Downward API для получения информации о Pod, Node, Namespace.
"""

import os
from dataclasses import dataclass


@dataclass
class KubernetesInfo:
    """Класс для хранения Kubernetes метаданных."""
    pod_name: str
    namespace: str
    node_name: str
    cpu_limit: str
    cpu_request: str
    memory_limit: str
    memory_request: str


def get_k8s_info() -> KubernetesInfo:
    """
    Получает Kubernetes метаданные из переменных окружения.
    
    Returns:
        KubernetesInfo объект с метаданными кластера
    """
    return KubernetesInfo(
        pod_name=os.getenv('HOSTNAME', 'unknown'),
        namespace=os.getenv('POD_NAMESPACE', 'default'),
        node_name=os.getenv('NODE_NAME', 'unknown'),
        cpu_limit=os.getenv('CPU_LIMIT', 'not set'),
        cpu_request=os.getenv('CPU_REQUEST', 'not set'),
        memory_limit=os.getenv('MEMORY_LIMIT', 'not set'),
        memory_request=os.getenv('MEMORY_REQUEST', 'not set'),
    )
