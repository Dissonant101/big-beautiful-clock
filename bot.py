import discord
from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv

class CustomBotClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="$", intents=discord.Intents.all(),
                         application_id=1038209909541589032)
        self.instances_channel = 1038276557925531749
        self.instances = {"clocks": [], "timers": [], "stopwatches": []}
        self.times = {"stopwatches": [], "timers": []}

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        await self.load_extension("cogs.clock")
        await self.load_extension("cogs.timer")
        await self.load_extension("cogs.stopwatch")
        await bot.tree.sync(guild=discord.Object(id=1038187258165067836))

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        print(f"{self.user.name} is ready to rumble!")
        async for message in self.get_channel(self.instances_channel).history():
            variant, channel_id, message_id = message.content.split()
            channel_id, message_id = int(channel_id), int(message_id)
            try:
                await self.get_channel(channel_id).fetch_message(message_id)
                if variant == "c":
                    self.instances["clocks"].append(
                        (channel_id, message_id))
                elif variant == "t":
                    self.instances["timers"].append(
                        (channel_id, message_id))
                elif variant == "s":
                    self.instances["stopwatches"].append(
                        (channel_id, message_id))
            except:
                await message.delete()


if __name__ == "__main__":
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    bot = CustomBotClient()
    bot.run(DISCORD_TOKEN)
