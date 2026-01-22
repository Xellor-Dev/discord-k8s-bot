import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import COMMAND_PREFIX, BOT_ACTIVITY_NAME
from logger import setup_logger
from services.metrics import MetricsCollector
from commands import ping

logger = setup_logger("bot")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    logger.info(f'Bot {bot.user.name} ready! ID: {bot.user.id}')
    MetricsCollector()
    logger.info("MetricsCollector initialized")
    await bot.change_presence(activity=discord.Game(name=BOT_ACTIVITY_NAME))
    logger.info(f'Bot status set: {BOT_ACTIVITY_NAME}')


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    logger.error(f"Command error {ctx.command}: {error}", exc_info=True)
    await ctx.send(f"❌ Error: {str(error)}")


def main():
    if not TOKEN:
        logger.error("DISCORD_TOKEN not found in environment!")
        print("❌ Error: DISCORD_TOKEN not found!")
        return
    
    ping.setup(bot)
    logger.info("Commands registered: !ping")
    
    try:
        logger.info("Starting bot...")
        bot.run(TOKEN)
    except KeyboardInterrupt:
        logger.info("Shutdown signal received (Ctrl+C)")
    except Exception as e:
        logger.error(f"Critical error: {e}", exc_info=True)
    finally:
        logger.info("Bot stopped")


if __name__ == "__main__":
    main()