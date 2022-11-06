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
    
    @discord.ui.button(style=discord.ButtonStyle.success, emoji="<:playbutton:1038622710252699700>")
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.inactive_timers[self.ids] = (self.inactive_timers[self.ids][0], self.inactive_timers[self.ids][1], dt.datetime.now())
            self.active_timers[self.ids] = self.inactive_timers[self.ids]
            self.inactive_timers.pop(self.ids)
        except:
            pass
        finally:
            print(self.active_timers)
            print(self.inactive_timers)
            await interaction.response.defer()
    
    @discord.ui.button(style=discord.ButtonStyle.red, emoji="<:pausebutton:1038624262820474900>")
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.active_timers[self.ids] = (self.active_timers[self.ids][0], self.active_timers[self.ids][1] + dt.datetime.now() - self.active_timers[self.ids][2], self.active_timers[self.ids][2])
            self.inactive_timers[self.ids] = self.active_timers[self.ids]
            self.active_timers.pop(self.ids)
        except:
            pass
        finally:
            print(self.active_timers)
            print(self.inactive_timers)
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
    @app_commands.describe(hours="Number of hours", minutes="Number of minutes", seconds="Number of seconds")
    async def create_timer(self, interaction: discord.Interaction, hours: str, minutes: str, seconds: str):
        hours, minutes, seconds = int(hours), int(minutes), int(seconds)
        initial_duration = dt.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        elapsed_time = dt.timedelta()
        now = dt.datetime.now()
        await interaction.response.defer()
        button = ButtonHandler(self.active_timers, self.inactive_timers)
        message = await interaction.followup.send(f"Loading timer!", view=button)
        button.set_ids(interaction.channel_id, message.id)
        key = (interaction.channel_id, message.id)
        self.active_timers[key] = (initial_duration, elapsed_time, now)
        await message.edit(content=self.get_display_time(self.active_timers[key]))
    
    @tasks.loop(seconds=2.0)
    async def update_timers(self):
        keys = tuple(self.active_timers.keys())
        for key in keys:
            try:
                message = await self.bot.get_channel(key[0]).fetch_message(key[1])
                if self.active_timers[key][2] + self.active_timers[key][0] - dt.datetime.now() <= dt.timedelta(0):
                    await message.edit(content=self.generator.generate_string((0, 0, 0)))
                    await self.bot.get_channel(key[0]).send(f"@everyone **Time's up!**")
                    self.inactive_timers[key] = self.active_timers[key]
                    self.active_timers.pop(key)
                else:
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
