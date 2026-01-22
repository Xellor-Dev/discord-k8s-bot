"""
Discord Kubernetes Bot - главный файл.
Отрефакторенная версия с модульной архитектурой.
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import COMMAND_PREFIX, BOT_ACTIVITY_NAME
from logger import setup_logger
from services.metrics import MetricsCollector
from commands import ping

# Настройка логирования
logger = setup_logger("bot")

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Настройка intents
intents = discord.Intents.default()
intents.message_content = True

# Создание экземпляра бота
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    """Событие при успешном запуске бота."""
    logger.info(f'Бот {bot.user.name} готов! ID: {bot.user.id}')
    
    # Инициализируем MetricsCollector (синглтон)
    MetricsCollector()
    logger.info("MetricsCollector инициализирован")
    
    # Устанавливаем статус бота
    await bot.change_presence(activity=discord.Game(name=BOT_ACTIVITY_NAME))
    logger.info(f'Статус бота установлен: {BOT_ACTIVITY_NAME}')


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    """Обработчик ошибок команд."""
    logger.error(f"Ошибка при выполнении команды {ctx.command}: {error}", exc_info=True)
    await ctx.send(f"❌ Произошла ошибка: {str(error)}")


def main():
    """Главная функция запуска бота."""
    if not TOKEN:
        logger.error("DISCORD_TOKEN не найден в переменных окружения!")
        print("❌ Ошибка: DISCORD_TOKEN не найден!")
        return
    
    # Регистрируем команды
    ping.setup(bot)
    logger.info("Команды зарегистрированы: !ping")
    
    # Запускаем бота
    try:
        logger.info("Запуск бота...")
        bot.run(TOKEN)
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки (Ctrl+C)")
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {e}", exc_info=True)
    finally:
        logger.info("Бот остановлен")


if __name__ == "__main__":
    main()