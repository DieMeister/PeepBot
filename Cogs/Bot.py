from discord.ext import commands
from discord.ext.commands import ExtensionFailed, ExtensionNotLoaded, ExtensionNotFound, NoEntryPointError


class Bot(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def sync(self, ctx) -> None:  # TODO check if user is allowed to execute command
        await self.bot.tree.sync()
        await ctx.send("Commands synced")

    @commands.command()
    async def reload_cog(self, ctx, cog: str) -> None:  # TODO check if user is allowed to execute command
        try:
            await self.bot.reload_extension(f"Cogs.{cog}")
            await ctx.send("Cog reloaded successfully")
        except (ExtensionFailed, ExtensionNotLoaded, ExtensionNotFound, NoEntryPointError):
            await ctx.send("Cog could not be reloaded")  # TODO differentiate between errors


async def setup(bot) -> None:
    await bot.add_cog(Bot(bot))