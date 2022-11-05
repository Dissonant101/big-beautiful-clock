import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime as dt
from helpers.generate_time import GenerateTimeString
import pytz


class Clock(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.generator = GenerateTimeString()
        self.update_clocks.start()

    def cog_unload(self):
        self.update_clocks.cancel()
        
    def get_current_time_string(self):
        parsed_time = self.generator.parse_time_object(dt.datetime.now(pytz.utc))
        return self.generator.generate_string(parsed_time)

    @app_commands.command(name="create_clock", description="Creates a clock!")
    @app_commands.describe(timezone="Your timezone")
    @app_commands.choices(timezone=app_commands.Choice(name="blah", value=123))
    async def create_clock(self, interaction: discord.Interaction, timezone: int):
        await interaction.response.defer()
        message = await interaction.followup.send(f"Loading clock!")
        await message.edit(content=self.get_current_time_string())
        await self.bot.get_channel(self.bot.instances_channel).send(f"c {interaction.channel_id} {message.id}")
        self.bot.instances["clocks"].append([interaction.channel_id, message.id])
    
    @tasks.loop(seconds=5.0)
    async def update_clocks(self):
        for i in range(len(self.bot.instances["clocks"])):
            channel_id, message_id = self.bot.instances["clocks"][i]
            
            try:
                message = await self.bot.get_channel(channel_id).fetch_message(message_id)
                await message.edit(content=self.get_current_time_string())
            except:
                self.bot.instances["clocks"].pop(i)
            
    @update_clocks.before_loop
    async def before_update_clocks(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Clock(bot), guilds=[discord.Object(id=1038187258165067836)])
