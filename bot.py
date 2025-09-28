import os
from dotenv import load_dotenv

import hikari
import lightbulb
import logging

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("Put DISCORD_TOKEN in a .env next to bot.py")

bot = hikari.GatewayBot(TOKEN)
client = lightbulb.client_from_app(bot, default_enabled_guilds=['1037174936046944297'])

@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    # Load any extensions
    await client.load_extensions("extensions.bart", "extensions.ping")
    # Start the bot - make sure commands are synced properly
    await client.start()

@bot.listen(hikari.InteractionCreateEvent)
async def on_interaction(e: hikari.InteractionCreateEvent) -> None:
    logging.info("Interaction received: %s", type(e.interaction).__name__)

bot.run()