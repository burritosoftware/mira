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

@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    # Load any extensions
    await client.load_extensions("extensions.bart")
    # Start the bot and sync commands
    await client.start()

if __name__ == "__main__":
    bot.run()
