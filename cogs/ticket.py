import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
from datetime import datetime
import os
import time
import chat_exporter


class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(CreateButton(self.bot))
        self.bot.add_view(CloseButton(self.bot))
        self.bot.add_view(TrashButton(self.bot))

    @commands.command(name="ticket")
    @commands.has_permissions(administrator=True)
    async def ticket(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                description="Nếu bạn cần hỗ trợ hãy ấn create ticket!"
            ),
            view=CreateButton(self.bot)
        )

async def get_transcript(member: discord.Member, channel: discord.TextChannel):
    export = await chat_exporter.export(channel=channel)
    file_name = f"{member.id}.html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(export)

def upload(file_path: str, member_name: str):
    # Đường dẫn tới thư mục cụ thể mà bạn muốn lưu file
    directory = "C:/Users/PC/Desktop/bot discord/bot-music/ticket-history"

    # Kiểm tra nếu thư mục chưa tồn tại, thì tạo nó
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Tạo tên file mới dựa trên timestamp
    file_name = f"{int(time.time())}.html"

    # Di chuyển và đổi tên file tới thư mục mới
    full_path = os.path.join(directory, file_name)
    os.rename(file_path, full_path)
    
    return file_name

async def send_log(title: str, guild: discord.Guild, description: str, color: discord.Color):
    log_channel = guild.get_channel(1278935420637417514)  # Thay bằng ID kênh của bạn
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    await log_channel.send(embed=embed)

class CreateButton(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.blurple, emoji="🎫", custom_id="ticketopen")
    async def ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        category = discord.utils.get(interaction.guild.categories, id=1278931299708567592)  # Thay bằng ID category của bạn
        for ch in category.text_channels:
            if ch.topic == f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!":
                await interaction.followup.send("You already have a ticket in {0}".format(ch.mention), ephemeral=True)
                return

        r1 = interaction.guild.get_role(1272774278789599334)  # Thay bằng ID role của bạn
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await category.create_text_channel(
            name=str(interaction.user),
            topic=f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!",
            overwrites=overwrites
        )
        await channel.send(
            embed=discord.Embed(
                title="Ticket Created!",
                description="Don't ping a staff member, they will be here soon.",
                color=discord.Color.green()
            ),
            view=CloseButton(self.bot)
        )
        await interaction.followup.send(
            embed=discord.Embed(
                description="Created your ticket in {0}".format(channel.mention),
                color=discord.Color.blurple()
            ),
            ephemeral=True
        )

        await send_log(
            title="Ticket Created",
            description="Created by {0}".format(interaction.user.mention),
            color=discord.Color.green(),
            guild=interaction.guild
        )

class CloseButton(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(label="Close the ticket", style=discord.ButtonStyle.red, custom_id="closeticket", emoji="🔒")
    async def close(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send("Closing this ticket in 3 seconds!")
        await asyncio.sleep(3)

        category = discord.utils.get(interaction.guild.categories, id=1278931356675477547)  # Thay bằng ID category của bạn
        r1 = interaction.guild.get_role(1272774278789599334)  # Thay bằng ID role của bạn
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        await interaction.channel.edit(category=category, overwrites=overwrites)
        await interaction.channel.send(
            embed=discord.Embed(
                description="Ticket Closed!",
                color=discord.Color.red()
            ),
            view=TrashButton(self.bot)
        )

        member = interaction.guild.get_member(int(interaction.channel.topic.split(" ")[0]))
        await get_transcript(member=member, channel=interaction.channel)
        file_name = upload(f'{member.id}.html', member.name)
        link = f"https://yourdomain.com/tickets/{file_name}"
        await send_log(
            title="Ticket Closed",
            description=f"Closed by: {interaction.user.mention}\n[click for transcript]({link})",
            color=discord.Color.yellow(),
            guild=interaction.guild
        )

class TrashButton(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Delete the ticket", style=discord.ButtonStyle.red, emoji="🚮", custom_id="trash")
    async def trash(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        await interaction.channel.send("Deleting the ticket in 3 seconds")
        await asyncio.sleep(3)
        await interaction.channel.delete()

        await send_log(
            title="Ticket Deleted",
            description=f"Deleted by {interaction.user.mention}, ticket: {interaction.channel.name}",
            color=discord.Color.red(),
            guild=interaction.guild
        )

async def setup(bot):
    await bot.add_cog(TicketCog(bot))
