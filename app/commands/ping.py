"""
Команда !ping - проверка задержки бота.
"""

from discord.ext import commands
from services.metrics import MetricsCollector


async def ping_command(ctx: commands.Context, bot: commands.Bot):
    """
    Обработчик команды !ping.
    
    Args:
        ctx: Контекст команды Discord
        bot: Экземпляр бота
    """
    metrics = MetricsCollector()
    
    # Увеличиваем счетчик команд
    metrics.increment_command_counter()
    
    # Получаем текущую задержку
    latency_ms = round(bot.latency * 1000)
    
    # Записываем в историю
    metrics.record_latency(latency_ms)
    
    # Отправляем ответ
    await ctx.send(f'Pong! 🚀 CI/CD работает! Latency: {latency_ms}ms')


def setup(bot: commands.Bot):
    """Регистрация команды !ping."""
    @bot.command(name='ping')
    async def ping(ctx: commands.Context):
        await ping_command(ctx, bot)
