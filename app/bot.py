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

# === Глобальные метрики ===
commands_executed = 0
api_latency_list = []

# === Kubernetes переменные окружения ===
K8S_POD_NAME = os.getenv('HOSTNAME', 'unknown')
K8S_NAMESPACE = os.getenv('POD_NAMESPACE', 'default')
K8S_NODE_NAME = os.getenv('NODE_NAME', 'unknown')
K8S_CPU_LIMIT = os.getenv('CPU_LIMIT', 'not set')
K8S_MEMORY_LIMIT = os.getenv('MEMORY_LIMIT', 'not set')
K8S_CPU_REQUEST = os.getenv('CPU_REQUEST', 'not set')
K8S_MEMORY_REQUEST = os.getenv('MEMORY_REQUEST', 'not set')

# Получаем начальные сетевые статистики
net_io_start = psutil.net_io_counters()
disk_io_start = psutil.disk_io_counters()

@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} готов! ID: {bot.user.id}')
    # Меняем статус бота на "Играет в Kubernetes"
    await bot.change_presence(activity=discord.Game(name="в Kubernetes GKE"))

@bot.command(name='ping')
async def ping(ctx):
    global commands_executed, api_latency_list
    commands_executed += 1
    latency = round(bot.latency * 1000)
    api_latency_list.append(latency)
    if len(api_latency_list) > 100:  # Храним последние 100 пингов
        api_latency_list.pop(0)
    await ctx.send(f'Pong! 🚀 CI/CD работает! Latency: {latency}ms')

@bot.command(name='info')
async def info(ctx):
    global commands_executed, api_latency_list, net_io_start, disk_io_start
    commands_executed += 1
    
    # === Временные метрики ===
    uptime = str(timedelta(seconds=int(time.time() - start_time)))
    
    # === CPU метрики ===
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=False)  # физические ядра
    cpu_count_logical = psutil.cpu_count(logical=True)  # логические ядра
    cpu_freq = psutil.cpu_freq()
    cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
    
    # === RAM метрики ===
    ram_info = psutil.virtual_memory()
    ram_usage = ram_info.percent
    ram_used = ram_info.used // (1024**3)  # ГБ
    ram_total = ram_info.total // (1024**3)  # ГБ
    
    # === Процесс метрики ===
    process = psutil.Process()
    process_memory = process.memory_info().rss // (1024**2)  # МБ
    
    # === Сетевые метрики ===
    net_io = psutil.net_io_counters()
    net_bytes_sent = (net_io.bytes_sent - net_io_start.bytes_sent) // (1024**2)  # МБ
    net_bytes_recv = (net_io.bytes_recv - net_io_start.bytes_recv) // (1024**2)  # МБ
    
    # === Disk I/O метрики ===
    disk_io = psutil.disk_io_counters()
    disk_read = (disk_io.read_bytes - disk_io_start.read_bytes) // (1024**2)  # МБ
    disk_write = (disk_io.write_bytes - disk_io_start.write_bytes) // (1024**2)  # МБ
    
    # === API метрики ===
    bot_latency = round(bot.latency * 1000)
    avg_latency = round(sum(api_latency_list) / len(api_latency_list)) if api_latency_list else 0
    
    # === Информация о боте ===
    guild_count = len(bot.guilds)
    total_members = sum(guild.member_count for guild in bot.guilds) if bot.guilds else 0
    
    # === Информация о системе ===
    cpu_type = platform.processor() or "Unknown"
    os_name = platform.system()
    os_version = platform.release()
    
    # === ПЕРВЫЙ EMBED: БОТ, DISCORD, K8S ===
    embed1 = discord.Embed(
        title="📊 Статус Kubernetes Pod (1/2)",
        description="Информация о боте и Kubernetes",
        color=0x326ce5
    )
    
    # БОТ И АПТАЙМ
    embed1.add_field(name="🤖 Бот", value=bot.user.name, inline=True)
    embed1.add_field(name="⏱️ Аптайм", value=uptime, inline=True)
    embed1.add_field(name="📈 Команд выполнено", value=str(commands_executed), inline=True)
    
    # DISCORD/API МЕТРИКИ
    embed1.add_field(name="📡 Текущий пинг", value=f"{bot_latency}ms", inline=True)
    embed1.add_field(name="📊 Средний пинг", value=f"{avg_latency}ms", inline=True)
    embed1.add_field(name="🖥️ Серверы", value=f"{guild_count}", inline=True)
    embed1.add_field(name="👥 Пользователи", value=f"{total_members}", inline=True)
    embed1.add_field(name="🐍 Python", value=platform.python_version(), inline=True)
    embed1.add_field(name="🐧 ОС", value=f"{os_name} {os_version}", inline=True)
    
    # KUBERNETES
    embed1.add_field(name="☸️ Pod", value=K8S_POD_NAME, inline=True)
    embed1.add_field(name="📍 Namespace", value=K8S_NAMESPACE, inline=True)
    embed1.add_field(name="🖱️ Node", value=K8S_NODE_NAME, inline=True)
    embed1.add_field(name="🔴 CPU Limit", value=K8S_CPU_LIMIT, inline=True)
    embed1.add_field(name="🟡 CPU Request", value=K8S_CPU_REQUEST, inline=True)
    embed1.add_field(name="🔵 Mem Limit", value=K8S_MEMORY_LIMIT, inline=True)
    embed1.add_field(name="🟢 Mem Request", value=K8S_MEMORY_REQUEST, inline=True)
    
    # CPU ОСНОВНОЕ
    embed1.add_field(name="⚙️ CPU Type", value=cpu_type, inline=True)
    embed1.add_field(name="🧠 CPU Load", value=f"{cpu_usage}%", inline=True)
    embed1.add_field(name="📌 CPU Cores", value=f"{cpu_count}физ/{cpu_count_logical}логи", inline=True)
    
    embed1.set_footer(text=f"Pod: {K8S_POD_NAME} | Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    embed1.set_thumbnail(url="https://kubernetes.io/images/favicon.png")
    
    # === ВТОРОЙ EMBED: РЕСУРСЫ ===
    embed2 = discord.Embed(
        title="📈 Ресурсы и Метрики (2/2)",
        description="CPU, Память, Сеть, Disk I/O",
        color=0x326ce5
    )
    
    # CPU ДЕТАЛИ
    cpu_cores_str = " | ".join([f"C{i}:{core}%" for i, core in enumerate(cpu_per_core[:6])])
    if len(cpu_per_core) > 6:
        cpu_cores_str += f"|+{len(cpu_per_core)-6}"
    embed2.add_field(name="🔥 CPU по ядрам", value=cpu_cores_str, inline=False)
    embed2.add_field(name="⚡ CPU Freq", value=f"{cpu_freq.current:.0f} MHz", inline=True)
    
    # ПАМЯТЬ
    embed2.add_field(name="💾 RAM Бота", value=f"{process_memory}MB", inline=True)
    embed2.add_field(name="🔋 RAM Система", value=f"{ram_used}/{ram_total}GB ({ram_usage}%)", inline=True)
    embed2.add_field(name="📊 RAM Free", value=f"{ram_info.available // (1024**3)}GB", inline=True)
    
    # СЕТЬ
    embed2.add_field(name="📤 Sent (с запуска)", value=f"{net_bytes_sent}MB", inline=True)
    embed2.add_field(name="📥 Recv (с запуска)", value=f"{net_bytes_recv}MB", inline=True)
    embed2.add_field(name="🔄 Total Network", value=f"{net_bytes_sent + net_bytes_recv}MB", inline=True)
    
    # DISK I/O
    embed2.add_field(name="💿 Disk Read", value=f"{disk_read}MB", inline=True)
    embed2.add_field(name="💿 Disk Write", value=f"{disk_write}MB", inline=True)
    embed2.add_field(name="💿 Disk Total I/O", value=f"{disk_read + disk_write}MB", inline=True)
    
    embed2.set_footer(text=f"Node: {K8S_NODE_NAME} | Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    embed2.set_thumbnail(url="https://kubernetes.io/images/favicon.png")

    await ctx.send(embeds=[embed1, embed2])

if __name__ == "__main__":
    if not TOKEN:
        print("Ошибка: Токен не найден!")
    else:
        bot.run(TOKEN)