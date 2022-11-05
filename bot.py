import discord
from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv


class CustomBotClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="$", intents=discord.Intents.all(), application_id=1038209909541589032)
        self.instances_channel = 1038276557925531749
        self.instances = []
    
    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        await self.load_extension("cogs.create_clock")
        await bot.tree.sync(guild=discord.Object(id=1038187258165067836))
    
    async def close(self):
        await super().close()
        await self.session.close()
    
    async def on_ready(self):
        print(f"{self.user.name} is ready to rumble!")
        async for msg in self.get_channel(self.instances_channel).history():
            self.instances.append(int(msg.content))


if __name__ == "__main__":
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    bot = CustomBotClient()
    bot.run(DISCORD_TOKEN)