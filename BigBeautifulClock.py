import interactions
import os
from dotenv import load_dotenv

class CustomBotClient(interactions.Client):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    bot = interactions.Client(token=DISCORD_TOKEN)
    
    bot.start()