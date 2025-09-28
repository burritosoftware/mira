import lightbulb

loader = lightbulb.Loader()

@loader.command
class Ping(lightbulb.SlashCommand, name="ping", description="Basic ping command"):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond("pong")