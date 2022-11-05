import discord
from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv


class CustomBotClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="$", intents=discord.Intents.all(), application_id=1038209909541589032)
        self.instances_channel = 1038276557925531749
        self.instances = {"clocks": [], "timers": [], "stopwatches": []}
    
    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        await self.load_extension("cogs.create_clock")
        await bot.tree.sync(guild=discord.Object(id=1038187258165067836))
    
    async def close(self):
        await super().close()
        await self.session.close()
    
    async def on_ready(self):
        print(f"{self.user.name} is ready to rumble!")
        async for message in self.get_channel(self.instances_channel).history():
            message_data = message.content.split()
            if message_data[0] == "c":
                self.instances["clocks"].append((int(message_data[1]), int(message_data[2])))
            elif message_data[0] == "t":
                self.instances["timers"].append((int(message_data[1]), int(message_data[2])))
            elif message_data[0] == "s":
                self.instances["stopwatches"].append((int(message_data[1]), int(message_data[2])))


if __name__ == "__main__":
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    bot = CustomBotClient()
    bot.run(DISCORD_TOKEN)