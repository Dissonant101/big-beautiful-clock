import discord
from discord import app_commands
from discord.ext import commands
import datetime as dt
from helpers.generate_time import GenerateTimeString


class CreateClock(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.generator = GenerateTimeString()

    @app_commands.command(name="create_clock", description="Creates a clock!")
    async def create_clock(self, interaction: discord.Interaction):
        await interaction.response.defer()
        message = await interaction.followup.send(f"Creating clock!")
        parsed_time = self.generator.parse_time_object(dt.datetime.now())
        await message.edit(content=self.generator.generate_string(parsed_time))
        await self.bot.get_channel(self.bot.instances_channel).send(message.id)
        self.bot.instances.append(message.id)


async def setup(bot):
    await bot.add_cog(CreateClock(bot), guilds=[discord.Object(id=1038187258165067836)])
