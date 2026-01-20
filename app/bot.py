import os
import discord
import platform
import psutil
import time
from datetime import timedelta
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
start_time = time.time()

@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} готов! ID: {bot.user.id}')
    # Меняем статус бота на "Играет в Kubernetes"
    await bot.change_presence(activity=discord.Game(name="в Kubernetes GKE"))

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong! 🚀 CI/CD работает!')

@bot.command(name='info')
async def info(ctx):
    # Собираем данные
    uptime = str(timedelta(seconds=int(time.time() - start_time)))
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    
    # Создаем Embed (Карточку)
    embed = discord.Embed(
        title="📊 Статус Kubernetes Pod",
        description="Информация о контейнере, в котором я запущен.",
        color=0x326ce5 # Официальный синий цвет Kubernetes
    )
    
    embed.add_field(name="🤖 Бот", value=bot.user.name, inline=True)
    embed.add_field(name="⏱️ Аптайм", value=uptime, inline=True)
    embed.add_field(name="🐧 Система", value=platform.system(), inline=True)
    
    embed.add_field(name="🧠 CPU Load", value=f"{cpu_usage}%", inline=True)
    embed.add_field(name="💾 RAM Usage", value=f"{ram_usage}%", inline=True)
    embed.add_field(name="🐍 Python", value=platform.python_version(), inline=True)
    
    embed.set_footer(text=f"Pod: {platform.node()} | Hosted on GKE")
    embed.set_thumbnail(url="https://kubernetes.io/images/favicon.png") # Лого K8s

    await ctx.send(embed=embed)

if __name__ == "__main__":
    if not TOKEN:
        print("Ошибка: Токен не найден!")
    else:
        bot.run(TOKEN)