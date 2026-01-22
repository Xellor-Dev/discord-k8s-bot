from discord.ext import commands
from services.metrics import MetricsCollector


async def ping_command(ctx: commands.Context, bot: commands.Bot):
    metrics = MetricsCollector()
    metrics.increment_command_counter()
    
    latency_ms = round(bot.latency * 1000)
    metrics.record_latency(latency_ms)
    
    await ctx.send(f'Pong! 🚀 CI/CD is working! Latency: {latency_ms}ms')


def setup(bot: commands.Bot):
    @bot.command(name='ping')
    async def ping(ctx: commands.Context):
        await ping_command(ctx, bot)
