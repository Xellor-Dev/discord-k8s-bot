import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# 1. Загружаем переменные из .env файла (для локального запуска)
load_dotenv()

# 2. Получаем токен из окружения
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("Ошибка: Токен не найден! Укажи DISCORD_TOKEN в переменных окружения.")
    exit(1)

# 3. Настройка намерений (Intents) - бот должен слышать сообщения
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} успешно подключился и готов к работе!')

@bot.command(name='ping')
async def ping(ctx):
    # Простая проверка жизни
    await ctx.send('Pong! 🏓 Я работаю внутри Kubernetes (почти)!')

# 4. Запуск
bot.run(TOKEN)