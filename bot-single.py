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
bot.subscribe(hikari.StartingEvent, client.start)

from helpers import (
    lucent,
    naturalreaders
)

@client.register
class George(
    lightbulb.SlashCommand,
    name="george",
    description="Speak using George's voice",
):
    text = lightbulb.string("text", 'What you want George to say')

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.defer()
        wav = await lucent.synthesize(text=self.text, voice="John-TED :: John-TED")
        await ctx.respond(attachments=[hikari.Bytes(wav, "george.wav")])

@client.register
class Gracie(
    lightbulb.SlashCommand,
    name="gracie",
    description="Speak using Gracie's voice",
):
    text = lightbulb.string("text", 'What you want Gracie to say')

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.defer()
        wav = await lucent.synthesize(text=self.text, voice="Grace-TED :: Grace-TED")
        await ctx.respond(attachments=[hikari.Bytes(wav, "gracie.wav")])

@client.register
class Sharon(
    lightbulb.SlashCommand,
    name="sharon",
    description="Speak using Sharon's voice",
):
    text = lightbulb.string("text", 'What you want Sharon to say')

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.defer()
        wav = await naturalreaders.synthesize(text=self.text, voice="21")
        await ctx.respond(attachments=[hikari.Bytes(wav, "sharon.mp3")])


bot.run()