import discord
from discord import app_commands
from discord.ext import commands
import datetime as dt


class CreateClock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="create_clock", description="Creates a clock!")
    async def create_clock(self, interaction):
        await interaction.response.defer()
        message = await interaction.followup.send(f"Creating clock!")
        await message.edit(content=dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


async def setup(bot):
    await bot.add_cog(CreateClock(bot), guilds=[discord.Object(id=1038187258165067836)])