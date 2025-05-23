import discord
from discord.ext import commands
import yt_dlp as youtube_dl

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("MusicCog đã được khởi tạo!")

    @discord.app_commands.command(name='join', description='Tham gia kênh voice hiện tại của người dùng')
    async def join(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message("Bạn cần phải vào kênh voice trước!")
            return
        channel = interaction.user.voice.channel
        await channel.connect()
        await interaction.response.send_message("Đã tham gia kênh voice!")

    @discord.app_commands.command(name='leave', description='Rời khỏi kênh voice')
    async def leave(self, interaction: discord.Interaction):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if voice_client:
            await voice_client.disconnect()
            await interaction.response.send_message("Đã rời khỏi kênh voice!")
        else:
            await interaction.response.send_message("Bot không có trong kênh voice!")

    @discord.app_commands.command(name='play', description='Phát nhạc từ YouTube bằng URL')
    async def play(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer()  # Thông báo rằng bot đang xử lý

        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if not voice_client:
            await interaction.followup.send("Bot chưa tham gia kênh voice!")
            return

        if voice_client.is_playing():
            voice_client.stop()  # Dừng phát nhạc hiện tại

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'quiet': True,
                'outtmpl': '%(id)s.%(ext)s',
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = None
                if 'formats' in info:
                    formats = [f for f in info['formats'] if f.get('acodec') != 'none']
                    if formats:
                        url2 = formats[0].get('url')
                if not url2:
                    url2 = info.get('url')
                    
                if not url2:
                    await interaction.followup.send("Không tìm thấy URL âm thanh.")
                    return

                voice_client.play(discord.FFmpegPCMAudio(
                    executable="C:/ffmpeg-7.0.2-full_build/bin/ffmpeg.exe",
                    source=url2,
                    before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
                ))
                await interaction.followup.send(f"Đang phát: {info['title']}")
        except Exception as e:
            await interaction.followup.send(f"Lỗi khi phát nhạc: {str(e)}")

    @discord.app_commands.command(name='pause', description='Tạm dừng phát nhạc')
    async def pause(self, interaction: discord.Interaction):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("Đã tạm dừng phát nhạc!")
        else:
            await interaction.response.send_message("Không có nhạc đang phát!")

    @discord.app_commands.command(name='resume', description='Tiếp tục phát nhạc')
    async def resume(self, interaction: discord.Interaction):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await interaction.response.send_message("Tiếp tục phát nhạc!")
        else:
            await interaction.response.send_message("Không có nhạc nào bị tạm dừng!")

async def setup(bot):
    await bot.add_cog(MusicCog(bot))
