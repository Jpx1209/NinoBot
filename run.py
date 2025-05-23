import discord
from discord.ext import commands
import asyncio

# Đọc token từ file token.txt
with open('token.txt', 'r') as file:
    TOKEN = file.read().strip()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} đã sẵn sàng!')
    try:
        # Đồng bộ lệnh slash
        synced = await bot.tree.sync()
        print(f"Đã đồng bộ {len(synced)} lệnh slash")
        
        # Thay đổi tên và trạng thái bot
        await bot.user.edit(username="_Nino")  # Cập nhật tên bot
        await bot.change_presence(activity=discord.Game(name="   Bot create by hycrschan    "))  # Cập nhật trạng thái
        print("Tên bot và trạng thái đã được cập nhật.")
        
    except Exception as e:
        print(f"Đồng bộ lệnh thất bại: {e}")

async def setup():
    # Tải các cogs
    await bot.load_extension('cogs.music')
    await bot.load_extension('cogs.help')
    await bot.load_extension('cogs.wel')    
    await bot.load_extension('cogs.ticket')
    await bot.load_extension('cogs.bye')
    await bot.load_extension('cogs.userinfo')

# Chạy bot và tải các cogs
async def main():
    await setup()
    await bot.start(TOKEN)

# Chạy chương trình
asyncio.run(main())
