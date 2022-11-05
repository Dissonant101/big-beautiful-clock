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
        t -= 2
        return self.generator.generate_string(parsed_time)

    @app_commands.command(name="create_timer", description="Creates a timer!")
    @app_commands.describe(t = "Enter time in seconds")

    async def create_clock(self, t, interaction: discord.Interaction):
        try:
            t = int(t)
            await interaction.response.defer()
            message = await interaction.followup.send(f"Creating timer!")
            await message.edit(content=self.countdown())
            await self.bot.get_channel(self.bot.instances_channel).send(f"c {interaction.channel_id} {message.id}")
            self.bot.instances["timer"].append([interaction.channel_id, message.id])
        except ValueError:
            await interaction.followup.send("Enter a numeric value")
    
    async def update_timer(self):
        for i in range(len(self.bot.instances["timer"])):
            channel_id, message_id = self.bot.instances["timer"][i]
            
            try:
                message = await self.bot.get_channel(channel_id).fetch_message(message_id)
                await message.edit(content=self.countdown())
            except:
                self.bot.instances["timer"].pop(i)
            
            if t == 0:
                break
            
    @update_timer.before_loop
    async def before_update_timer(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Timer(bot), guilds=[discord.Object(id=1038187258165067836)])

