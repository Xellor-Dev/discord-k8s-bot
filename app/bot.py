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
    
    # === Кэш Discord ===
    guilds_cached = len(bot.guilds)
    users_cached = len(bot.cached_users) if hasattr(bot, 'cached_users') else 'N/A'
    
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
    
    # === Создаем Embed ===
    embed = discord.Embed(
        title="📊 Полный Статус Kubernetes Pod",
        description="Детальная информация о контейнере и боте.",
        color=0x326ce5
    )
    
    # === РАЗДЕЛ 1: БОТ И АПТАЙМ ===
    embed.add_field(name="🤖 Бот", value=bot.user.name, inline=True)
    embed.add_field(name="⏱️ Аптайм", value=uptime, inline=True)
    embed.add_field(name="📈 Команд выполнено", value=str(commands_executed), inline=True)
    
    # === РАЗДЕЛ 2: DISCORD/API МЕТРИКИ ===
    embed.add_field(name="📡 Текущий пинг", value=f"{bot_latency}ms", inline=True)
    embed.add_field(name="📊 Средний пинг", value=f"{avg_latency}ms", inline=True)
    embed.add_field(name="🖥️ Серверы", value=f"{guild_count}", inline=True)
    
    embed.add_field(name="👥 Пользователи", value=f"{total_members}", inline=True)
    embed.add_field(name="💾 Кэш гильдий", value=f"{guilds_cached}", inline=True)
    embed.add_field(name="🐍 Python", value=platform.python_version(), inline=True)
    
    # === РАЗДЕЛ 3: KUBERNETES ===
    embed.add_field(name="☸️ Pod Name", value=K8S_POD_NAME, inline=True)
    embed.add_field(name="📍 Namespace", value=K8S_NAMESPACE, inline=True)
    embed.add_field(name="🖱️ Node", value=K8S_NODE_NAME, inline=True)
    
    embed.add_field(name="🔴 CPU Limit", value=K8S_CPU_LIMIT, inline=True)
    embed.add_field(name="🟡 CPU Request", value=K8S_CPU_REQUEST, inline=True)
    embed.add_field(name="🔵 Memory Limit", value=K8S_MEMORY_LIMIT, inline=True)
    
    embed.add_field(name="🟢 Memory Request", value=K8S_MEMORY_REQUEST, inline=True)
    embed.add_field(name="🐧 ОС", value=f"{os_name} {os_version}", inline=True)
    embed.add_field(name="⚙️ CPU", value=f"{cpu_type}", inline=True)
    
    # === РАЗДЕЛ 4: CPU МЕТРИКИ ===
    embed.add_field(name="🧠 CPU Load (общий)", value=f"{cpu_usage}%", inline=True)
    embed.add_field(name="📌 CPU Ядра", value=f"{cpu_count} физ. / {cpu_count_logical} логич.", inline=True)
    embed.add_field(name="⚡ CPU Freq", value=f"{cpu_freq.current:.0f} MHz", inline=True)
    
    cpu_cores_str = " | ".join([f"Core {i}: {core}%" for i, core in enumerate(cpu_per_core[:4])])
    if len(cpu_per_core) > 4:
        cpu_cores_str += f" | +{len(cpu_per_core)-4} more"
    embed.add_field(name="🔥 CPU по ядрам", value=cpu_cores_str, inline=False)
    
    # === РАЗДЕЛ 5: ПАМЯТЬ ===
    embed.add_field(name="💾 RAM Бота (процесс)", value=f"{process_memory}MB", inline=True)
    embed.add_field(name="🔋 RAM Система", value=f"{ram_used}GB / {ram_total}GB ({ram_usage}%)", inline=True)
    embed.add_field(name="📊 RAM Доступно", value=f"{ram_info.available // (1024**3)}GB", inline=True)
    
    # === РАЗДЕЛ 6: СЕТЕВЫЕ МЕТРИКИ ===
    embed.add_field(name="📤 Отправлено (с запуска)", value=f"{net_bytes_sent}MB", inline=True)
    embed.add_field(name="📥 Получено (с запуска)", value=f"{net_bytes_recv}MB", inline=True)
    embed.add_field(name="🔄 Всего передачи", value=f"{net_bytes_sent + net_bytes_recv}MB", inline=True)
    
    # === РАЗДЕЛ 7: DISK I/O ===
    embed.add_field(name="💿 Disk Read (с запуска)", value=f"{disk_read}MB", inline=True)
    embed.add_field(name="💿 Disk Write (с запуска)", value=f"{disk_write}MB", inline=True)
    embed.add_field(name="💿 Disk Total I/O", value=f"{disk_read + disk_write}MB", inline=True)
    
    embed.set_footer(text=f"Pod: {K8S_POD_NAME} | Cluster: {K8S_NODE_NAME} | Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    embed.set_thumbnail(url="https://kubernetes.io/images/favicon.png")

    await ctx.send(embed=embed)

if __name__ == "__main__":
    if not TOKEN:
        print("Ошибка: Токен не найден!")
    else:
        bot.run(TOKEN)