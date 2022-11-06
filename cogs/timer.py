import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime as dt
from helpers.generate_time import GenerateTimeString


class ButtonHandler(discord.ui.View):
    def __init__(self, active_timers, inactive_timers):
        super().__init__()
        self.active_timers = active_timers
        self.inactive_timers = inactive_timers
        self.ids = None
    
    def set_ids(self, channel_id, message_id):
        self.ids = (channel_id, message_id)
    
    @discord.ui.button(label="Resume", style=discord.ButtonStyle.primary)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.inactive_timers[self.ids][2] = dt.datetime.now()
            self.active_timers[self.ids] = self.inactive_timers[self.ids].pop()
        except:
            pass
        finally:
            await interaction.response.defer()
    
    @discord.ui.button(label="Pause", style=discord.ButtonStyle.danger)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.active_timers[self.ids][1] += dt.datetime.now() - self.active_timers[self.ids][2]
            self.inactive_timers[self.ids] = self.active_timers[self.ids].pop()
        except:
            pass
        finally:
            await interaction.response.defer()
class Timer(commands.Cog):       
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.generator = GenerateTimeString()
        self.active_timers = {}
        self.inactive_timers = {}
        self.update_timers.start()

    def cog_unload(self):
        self.update_timers.cancel()
        
    def get_display_time(self, timer):
        initial_duration, elapsed_time, now = timer
        target = now + initial_duration - elapsed_time
        display_time = self.generator.parse_delta_object(target - dt.datetime.now())
        return self.generator.generate_string(display_time)
        
    @app_commands.command(name="create_timer", description="Creates a timer!")
    @app_commands.describe(days="Number of days", hours="Number of hours", minutes="Number of minutes", seconds="Number of seconds")
    async def create_timer(self, interaction: discord.Interaction, days: str, hours: str, minutes: str, seconds: str):
        days, hours, minutes, seconds = int(days), int(hours), int(minutes), int(seconds)
        initial_duration = dt.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        elapsed_time = dt.timedelta()
        now = dt.datetime.now()
        await interaction.response.defer()
        button = ButtonHandler(self.active_timers, self.inactive_timers)
        message = await interaction.followup.send(f"Loading timer!", view=button)
        button.set_ids(interaction.channel_id, message.id)
        key = (interaction.channel_id, message.id)
        self.active_timers[key] = [initial_duration, elapsed_time, now]
        await message.edit(content=self.get_display_time(self.active_timers[key]))
    
    @tasks.loop(seconds=5.0)
    async def update_timers(self):
        keys = tuple(self.active_timers.keys())
        for key in keys:
            try:
                message = await self.bot.get_channel(key[0]).fetch_message(key[1])
                await message.edit(content=self.get_display_time(self.active_timers[key]))
            except:
                try:
                    self.active_timers[key].pop()
                except:
                    pass
            
    @update_timers.before_loop
    async def before_update_timers(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Timer(bot), guilds=[discord.Object(id=1038187258165067836)])
