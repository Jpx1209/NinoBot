import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("HelpCog đã được khởi tạo!")

    @discord.app_commands.command(name='bothelp', description='Hiển thị thông tin về các lệnh của bot')
    async def bothelp(self, interaction: discord.Interaction):
        # Tạo Embed với tiêu đề và màu sắc
        embed = discord.Embed(
            title="Danh sách các lệnh của bot",
            description="",
            color=discord.Color.blue()  # Màu xanh cho viền
        )

        # Thêm các field cho từng lệnh
        embed.add_field(name="/join", value="Tham gia kênh voice hiện tại của người dùng.", inline=False)
        embed.add_field(name="/leave", value="Rời khỏi kênh voice.", inline=False)
        embed.add_field(name="/play <URL>", value="Phát nhạc từ YouTube bằng URL.", inline=False)
        embed.add_field(name="/pause", value="Tạm dừng phát nhạc.", inline=False)
        embed.add_field(name="/resume", value="Tiếp tục phát nhạc.", inline=False)
        embed.add_field(name="/bothelp", value="Hiển thị thông tin về các lệnh.", inline=False)
        embed.add_field(name="/userinfo", value="Hiển thị thông tin người dùng.", inline=False)

        # Gửi Embed trong message
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
