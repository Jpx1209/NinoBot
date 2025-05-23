import discord
from discord.ext import commands
from datetime import datetime


class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(1272774279133663265)  # Thay thế bằng ID kênh của bạn

        # Tạo embed
        em = discord.Embed(
            title='Welcome',
            description=f'{member.mention} đã gia nhập {member.guild.name}',
            color=discord.Color.blurple(),  # Thay đổi màu sắc nếu cần
        timestamp=datetime.utcnow()
        ).add_field(
            name='📜 Quy Tắc',
            value=f'<#1272774279133663269>'  # Thay thế bằng ID kênh quy tắc của bạn
        ).add_field(
            name='💬 Chat',
            value='<#1272774279439712370>'  # Thay thế bằng ID kênh chat của bạn
        ).set_image(url='attachment://wel.gif')  # Đặt ảnh GIF làm hình ảnh trong embed

        # Gửi embed và ảnh GIF
        # Đặt ảnh GIF vào file đính kèm
        with open(r'C:\Users\PC\Desktop\bot discord\bot-music\gif\wel.gif', 'rb') as f:
            await channel.send(embed=em, files=[discord.File(f, 'wel.gif')])

async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
