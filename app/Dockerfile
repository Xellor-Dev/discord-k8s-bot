# 1. Берем легкий официальный образ Python
FROM python:3.12-slim

# 2. Отключаем создание кеш-файлов .pyc (в контейнере они не нужны)
ENV PYTHONDONTWRITEBYTECODE=1
# 3. Вывод логов сразу в консоль (важно для docker logs)
ENV PYTHONUNBUFFERED=1

# 4. Создаем рабочую папку внутри контейнера
WORKDIR /app

# 5. Сначала копируем зависимости (хитрость для кеширования Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Теперь копируем сам код бота
COPY bot.py .

# 7. Команда запуска
CMD ["python", "bot.py"]