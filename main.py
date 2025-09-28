import os
from dotenv import load_dotenv

import hikari
import lightbulb

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("Put DISCORD_TOKEN in a .env next to bot.py")

bot = hikari.GatewayBot(TOKEN)
client = lightbulb.client_from_app(bot, default_enabled_guilds=['1037174936046944297'])

@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    await client.load_extensions("extensions.bart", "extensions.ping")

@bot.listen(hikari.StartedEvent)
async def on_started(_: hikari.StartedEvent) -> None:
    await client.start()

bot.run()
