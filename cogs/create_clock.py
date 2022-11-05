import discord
from discord import app_commands
from discord.ext import commands
import datetime as dt
from helpers.generate_time import GenerateTimeString

class CreateClock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.generator = GenerateTimeString()
    
    @app_commands.command(name="create_clock", description="Creates a clock!")
    async def create_clock(self, interaction):
        await interaction.response.defer()
        message = await interaction.followup.send(f"Creating clock!")
        parsed_time = self.generator.parse_time_object(dt.datetime.now())
        await message.edit(content=self.generator.generate_string(parsed_time, True))


async def setup(bot):
    await bot.add_cog(CreateClock(bot), guilds=[discord.Object(id=1038187258165067836)])