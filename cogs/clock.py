import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime as dt
from helpers.generate_time import GenerateTimeString
import pytz

TIMEZONES = [app_commands.Choice(name="Samoa Standard Time (UTC-11)", value="Etc/GMT+11"),
             app_commands.Choice(name="Hawaii Standard Time (UTC-10)", value="Etc/GMT+10"),
             app_commands.Choice(name="Alaska Standard Time (UTC-9)", value="Etc/GMT+9"),
             app_commands.Choice(name="Pacific Standard Time (UTC-8)", value="Etc/GMT+8"),
             app_commands.Choice(name="Mountain Standard Time (UTC-7)", value="Etc/GMT+7"),
             app_commands.Choice(name="Central Standard Time (UTC-6)", value="Etc/GMT+6"),
             app_commands.Choice(name="Eastern Standard Time (UTC-5)", value="Etc/GMT+5"),
             app_commands.Choice(name="Atlantic Standard Time (UTC-4)", value="Etc/GMT+4"),
             app_commands.Choice(name="Uruguay Standard Time (UTC-3)", value="Etc/GMT+3"),
             app_commands.Choice(name="South Georgia Standard Time (UTC-2)", value="Etc/GMT+2"),
             app_commands.Choice(name="Cape Verde Standard Time (UTC-1)", value="Etc/GMT+1"),
             app_commands.Choice(name="Greenwich Mean Time (UTC-0)", value="Etc/GMT-0"),
             app_commands.Choice(name="Central European Time (UTC+1)", value="Etc/GMT-1"),
             app_commands.Choice(name="Central Africa Time (UTC+2)", value="Etc/GMT-2"),
             app_commands.Choice(name="Moscow Standard Time (UTC+3)", value="Etc/GMT-3"),
             app_commands.Choice(name="Georgia Standard Time (UTC+4)", value="Etc/GMT-4"),
             app_commands.Choice(name="Pakistan Standard Time (UTC+5)", value="Etc/GMT-5"),
             app_commands.Choice(name="Bangladesh Standard Time (UTC+6)", value="Etc/GMT-6"),
             app_commands.Choice(name="Thailand Standard Time (UTC+7)", value="Etc/GMT-7"),
             app_commands.Choice(name="Western Standard Time (UTC+8)", value="Etc/GMT-8"),
             app_commands.Choice(name="Japan Standard Time (UTC+9)", value="Etc/GMT-9"),
             app_commands.Choice(name="Papua New Guinea Standard Time (UTC+10)", value="Etc/GMT-10"),
             app_commands.Choice(name="New Caledonia Standard Time (UTC+11)", value="Etc/GMT-11"),
             app_commands.Choice(name="New Zealand Standard Time (UTC+12)", value="Etc/GMT+12")]


class Clock(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.generator = GenerateTimeString()
        self.update_clocks.start()

    def cog_unload(self):
        self.update_clocks.cancel()
        
    def get_current_time_string(self, timezone):
        parsed_time = self.generator.parse_time_object(dt.datetime.now(pytz.timezone(timezone)))
        return self.generator.generate_string(parsed_time)

    @app_commands.command(name="create_clock", description="Creates a clock!")
    @app_commands.describe(timezone="Your timezone")
    @app_commands.choices(timezone=TIMEZONES)
    async def create_clock(self, interaction: discord.Interaction, timezone: str):
        await interaction.response.defer()
        message = await interaction.followup.send(f"Loading clock!")
        await message.edit(content=self.get_current_time_string(timezone))
        await self.bot.get_channel(self.bot.instances_channel).send(f"c {interaction.channel_id} {message.id} {timezone}")
        self.bot.instances["clocks"].append((interaction.channel_id, message.id, timezone))
    
    @tasks.loop(seconds=2.0)
    async def update_clocks(self):
        for i in range(len(self.bot.instances["clocks"])):
            channel_id, message_id, timezone = self.bot.instances["clocks"][i]
            
            try:
                message = await self.bot.get_channel(channel_id).fetch_message(message_id)
                await message.edit(content=self.get_current_time_string(timezone))
            except:
                self.bot.instances["clocks"].pop(i)
            
    @update_clocks.before_loop
    async def before_update_clocks(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Clock(bot), guilds=[discord.Object(id=1038187258165067836)])
