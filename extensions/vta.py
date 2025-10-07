import hikari
import lightbulb
import sys

sys.path.append("..")

from helpers import (
    sapi
)

loader = lightbulb.Loader()

@loader.command()
class Samantha(
    lightbulb.SlashCommand,
    name="samantha",
    description="Speak using Samantha's voice (VTA)",
):
    text = lightbulb.string("text", 'What you want Samantha to say')

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.defer()
        wav = await sapi.synthesize(text=self.text, voice="VEX_Samantha")
        await ctx.respond(attachments=[hikari.Bytes(wav, "samantha.wav")])