import os
from dotenv import load_dotenv

import hikari
import lightbulb

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("Put DISCORD_TOKEN in a .env next to bot.py")

bot = hikari.GatewayBot(TOKEN)
client = lightbulb.client_from_app(bot)
bot.subscribe(hikari.StartingEvent, client.start)

client.load_extensions("extensions")

if __name__ == "__main__":
    bot.run()
