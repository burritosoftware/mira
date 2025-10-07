import hikari
import lightbulb
import sys

sys.path.append("..")

from helpers import (
    sapi,
    naturalreaders
)

loader = lightbulb.Loader()

@loader.command()
class George(
    lightbulb.SlashCommand,
    name="george",
    description="Speak using George's voice (BART Platform)",
):
    text = lightbulb.string("text", 'What you want George to say')

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.defer()
        wav = await sapi.synthesize(text=self.text, voice="John-TED :: John-TED")
        await ctx.respond(attachments=[hikari.Bytes(wav, "george.wav")])

@loader.command()
class Gracie(
    lightbulb.SlashCommand,
    name="gracie",
    description="Speak using Gracie's voice (BART Platform)",
):
    text = lightbulb.string("text", 'What you want Gracie to say')

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.defer()
        wav = await sapi.synthesize(text=self.text, voice="Grace-TED :: Grace-TED")
        await ctx.respond(attachments=[hikari.Bytes(wav, "gracie.wav")])

@loader.command()
class Sharon(
    lightbulb.SlashCommand,
    name="sharon",
    description="Speak using Sharon's voice (BART Train)",
):
    text = lightbulb.string("text", 'What you want Sharon to say')

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.defer()
        wav = await naturalreaders.synthesize(text=self.text, voice="21")
        await ctx.respond(attachments=[hikari.Bytes(wav, "sharon.mp3")])
