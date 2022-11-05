import discord
from discord import app_commands
from discord.ext import commands
import datetime as dt
from helpers.generate_time import GenerateTimeString

class buttonHandler(discord.ui.View):
    def __init__(self, bot : commands.Bot):
        super().__init__(timeout = 60)
        self.message = None

    @discord.ui.button(label = "Default Emoji",
                       style = discord.ButtonStyle.success, 
                       emoji = "⬜")
    async def button1(self,
                      interaction:discord,interacton,
                      button: discord.ui.Button):
        parsed_time = self.generator.parse_time_object(dt.datetime.now())
        await interaction.response.send_message(content=self.generator.generate_string(parsed_time, True))
    
    async def on_timeout(self):
        self.message.edit("Timeout!", view = None)


class Buttons(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        
    
    @app_commands.command(name="commands", description="List of Commands")
    async def create_buttons(self, interaction : discord.Interaction):
        view = buttonHandler()
        await interaction.response.send_message("Choose the commands you want to execute", view = view)

async def setup(bot):
    await bot.add_cog(Buttons(bot), guilds=[discord.Object(id=1038187258165067836)])

        # message = await interaction.followup.send(f"Creating clock!")
        # parsed_time = self.generator.parse_time_object(dt.datetime.now())
        # await message.edit(content=self.generator.generate_string(parsed_time, True))