import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime as dt
from helpers.generate_time import GenerateTimeString


class ButtonHandler(discord.ui.View):
    @discord.ui.button(label="Resume", style=discord.ButtonStyle.primary)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="You clicked me!")
    
    @discord.ui.button(label="Pause", style=discord.ButtonStyle.primary)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="You clicked me!")


class Timer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.generator = GenerateTimeString()
        self.timers = {"active": set(), "inactive": set()}
        self.update_timers.start()

    def cog_unload(self):
        self.update_timers.cancel()
        
    def get_current_time_string(self):
        parsed_time = self.generator.parse_time_object(dt.datetime.now())
        return self.generator.generate_string(parsed_time)

    @app_commands.command(name="create_timer", description="Creates a timer!")
    @app_commands.describe(days="Number of days", hours="Number of hours", minutes="Number of minutes", seconds="Number of seconds")
    async def create_timer(self, interaction: discord.Interaction, days: str, hours: str, minutes: str, seconds: str):
        days, hours, minutes, seconds = int(days), int(hours), int(minutes), int(seconds)
        initial_duration = dt.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        elapsed_time = dt.timedelta()
        now = dt.datetime.now()
        self.timers["active"].add((initial_duration, elapsed_time, now))
        
        await interaction.response.defer()
        message = await interaction.followup.send(f"Loading timer!", view=ButtonHandler())
        await message.edit(content=self.get_current_time_string())
        await self.bot.get_channel(self.bot.instances_channel).send(f"c {interaction.channel_id} {message.id}")
        self.bot.instances["timers"].append([interaction.channel_id, message.id])
    
    @tasks.loop(seconds=5.0)
    async def update_timers(self):
        for i in range(len(self.bot.instances["timers"])):
            channel_id, message_id = self.bot.instances["timers"][i]
            
            try:
                message = await self.bot.get_channel(channel_id).fetch_message(message_id)
                await message.edit(content=self.get_current_time_string())
            except:
                self.bot.instances["timers"].pop(i)
            
    @update_timers.before_loop
    async def before_update_timers(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Timer(bot), guilds=[discord.Object(id=1038187258165067836)])
