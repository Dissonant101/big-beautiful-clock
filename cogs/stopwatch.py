import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime as dt
from helpers.generate_time import GenerateTimeString

st_run = False

class ButtonHandler(discord.ui.View):

    @discord.ui.button(style=discord.ButtonStyle.success, emoji="<:playbutton:1038622710252699700>")
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        global st_run
        st_run = True
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.red, emoji="<:pausebutton:1038624262820474900>")
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        global st_run
        st_run = False
        await interaction.response.defer()


class StopWatch():
    def __init__(self, channel_id, message_id) -> None:
        self.ids = (channel_id, message_id)
        self.time = [0, 0, 0]

    def updateTime(self, elapsedSeconds: int):
        self.time[2] += elapsedSeconds
        if self.time[2] > 60:
            self.time[1] += self.time[2]//60
            self.time[2] %= 60
        if self.time[1] > 60:
            self.time[0] += self.time[2]//60
            self.time[1] %= 60


class StopWatches(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.generator = GenerateTimeString()
        self.update_stopwatches.start()

    def cog_unload(self):
        self.update_stopwatches.cancel()

    @app_commands.command(name="create_stopwatch", description="Creates a stopwatch!")
    async def create_stopwatch(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.B = ButtonHandler()
        message = await interaction.followup.send(f"Loading stopwatch!", view=self.B)
        s = StopWatch(interaction.channel_id, message.id)
        
        await message.edit(content=self.generator.generate_string((s.time[0], s.time[1], s.time[2])))
        await self.bot.get_channel(self.bot.instances_channel).send(f"s {interaction.channel_id} {message.id}")
        self.bot.instances["stopwatches"].append([interaction.channel_id, message.id])
        self.bot.times["stopwatches"].append(s)

    @tasks.loop(seconds=2.0)
    async def update_stopwatches(self):
        if not st_run:
            return
        for i in range(len(self.bot.instances["stopwatches"])):
            channel_id, message_id = self.bot.instances["stopwatches"][i]
            try:
                message = await self.bot.get_channel(channel_id).fetch_message(message_id)

                s = self.bot.times["stopwatches"][i]
                s.updateTime(2)

                await message.edit(content=self.generator.generate_string((s.time[0], s.time[1], s.time[2])), view= self.B)
            except:
                self.bot.instances["stopwatches"].pop(i)
                for j in range(len(self.bot.times["stopwatches"])):
                    if self.bot.times["stopwatches"][j].ids == (channel_id, message_id):
                        self.bot.times["stopwatches"].pop(j)

    @update_stopwatches.before_loop
    async def before_update_stopwatches(self):
        await self.bot.wait_until_ready()



async def setup(bot):
    await bot.add_cog(StopWatches(bot), guilds=[discord.Object(id=1038187258165067836)])
