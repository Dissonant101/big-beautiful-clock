import discord
from discord.ext import commands
import interactions
import os
from dotenv import load_dotenv


class CustomBotClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="$", intents=discord.Intents.all())
    
    async def on_ready(self):
        print(f"{self.user.name} is ready to rumble!")


if __name__ == "__main__":
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    
    bot = CustomBotClient()
    bot.run(DISCORD_TOKEN)