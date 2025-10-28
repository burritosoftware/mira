import hikari
import lightbulb
import sys

sys.path.append("..")

from helpers import (
    sapi,
    naturalreaders,
    gtts
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
        mp3 = await naturalreaders.synthesize(text=self.text, voice="21")
        await ctx.respond(attachments=[hikari.Bytes(mp3, "sharon.mp3")])

@loader.command()
class Anna(
    lightbulb.SlashCommand,
    name="anna",
    description="Speak using Anna's voice (eBART Platform)",
):
    text = lightbulb.string("text", 'What you want Anna to say')

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.defer()
        wav = await sapi.synthesize(text=self.text, voice="Microsoft Anna")
        await ctx.respond(attachments=[hikari.Bytes(wav, "anna.wav")])

@loader.command()
class eBART(
    lightbulb.SlashCommand,
    name="ebart",
    description="Speak using the eBART voice (Google/eBART Train)",
):
    text = lightbulb.string("text", 'What you want the eBART voice to say')

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.defer()
        mp3 = await gtts.synthesize(text=self.text)
        await ctx.respond(attachments=[hikari.Bytes(mp3, "ebart.mp3")])