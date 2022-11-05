import time
import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime as dt
from helpers.generate_time import GenerateTimeString


class Timer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.generator = GenerateTimeString()
        self.update_timer.start()

    def cog_unload(self):
        self.update_timer.cancel()
        
    def countdown(self):
        global t 

        mins, secs = divmod(t, 60)
        hrs, mins = divmod(mins, 60)
        parsed_time = self.generator.parse_time_object((hrs,mins,secs))
        time.sleep(1)
        t -= 1
        return self.generator.generate_string(parsed_time)

    @app_commands.command(name="create_timer", description="Creates a timer!")
    async def create_clock(self, interaction: discord.Interaction):
        global t

        await interaction.send(f"Enter time in seconds")
        def check(t):
         return t.author == interaction.author and t.channel == interaction.channel and \
        t.content.lower()

        t = await interaction.wait_for("message", check=check)
        try:
            t = int(t.content.lower())
            await interaction.response.defer()
            message = await interaction.followup.send(f"Creating timer!")
            await message.edit(content=self.countdown())
            await self.bot.get_channel(self.bot.instances_channel).send(f"c {interaction.channel_id} {message.id}")
            self.bot.instances["timer"].append([interaction.channel_id, message.id])
        except ValueError:
            await interaction.followup.send("Enter a numeric value")
    
    @tasks.loop(seconds=2.0)
    async def update_timer(self):
        for channel_id, message_id in self.bot.instances["timer"]:
            message = await self.bot.get_channel(channel_id).fetch_message(message_id)
            await message.edit(content=self.countdown())
            
    @update_timer.before_loop
    async def before_update_timer(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Timer(bot), guilds=[discord.Object(id=1038187258165067836)])


