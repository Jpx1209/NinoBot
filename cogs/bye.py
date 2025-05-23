import discord
from discord.ext import commands
from datetime import datetime
import pytz

class GoodbyeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(1272774279133663267)  # Thay thế bằng ID kênh của bạn


        # Tạo embed
        em = discord.Embed(
            title='Goodbye',
            description=f'{member.name} đã rời khỏi {member.guild.name}',
            color=discord.Color.blurple(),  # Thay đổi màu sắc nếu cần
        timestamp=datetime.utcnow()
        ).add_field(
            name='👋 Chúng tôi sẽ nhớ bạn',
            value='Hy vọng bạn sẽ quay lại sớm!'
        ).set_image(url='attachment://bye.gif')  # Đặt ảnh GIF làm hình ảnh trong embed

        # Gửi embed và ảnh GIF
        # Sử dụng đường dẫn với dấu gạch chéo ngược và escape ký tự
        await channel.send(embed=em, files=[discord.File(r'C:\Users\PC\Desktop\bot discord\bot-music\gif\bye.gif')])

async def setup(bot):
    await bot.add_cog(GoodbyeCog(bot))
