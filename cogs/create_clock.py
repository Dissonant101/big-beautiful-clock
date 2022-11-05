import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime as dt
from helpers.generate_time import GenerateTimeString


class Clock(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.generator = GenerateTimeString()
        self.update_clocks.start()

    def cog_unload(self):
        self.update_clocks.cancel()
        
    def get_current_time_string(self):
        parsed_time = self.generator.parse_time_object(dt.datetime.now())
        return self.generator.generate_string(parsed_time)

    @app_commands.command(name="create_clock", description="Creates a clock!")
    async def create_clock(self, interaction: discord.Interaction):
        await interaction.response.defer()
        message = await interaction.followup.send(f"Creating clock!")
        await message.edit(content=self.get_current_time_string())
        await self.bot.get_channel(self.bot.instances_channel).send(f"c {interaction.channel_id} {message.id}")
        self.bot.instances["clocks"].append([interaction.channel_id, message.id])
    
    @tasks.loop(seconds=2.0)
    async def update_clocks(self):
        for channel_id, message_id in self.bot.instances["clocks"]:
            message = await self.bot.get_channel(channel_id).fetch_message(message_id)
            await message.edit(content=self.get_current_time_string())
            
    @update_clocks.before_loop
    async def before_update_clocks(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Clock(bot), guilds=[discord.Object(id=1038187258165067836)])
