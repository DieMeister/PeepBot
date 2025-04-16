from discord.ext import commands
from discord.ext.commands import ExtensionFailed, ExtensionNotLoaded, ExtensionNotFound, NoEntryPointError

import logic


class Bot(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def sync(self, ctx) -> None:  # TODO check if user is allowed to execute command
        await self.bot.tree.sync()
        logic.logging("info", "bot", "Commands synced", {})
        await ctx.reply("Commands synced")

    @commands.command()
    async def reload_cog(self, ctx, cog: str) -> None:  # TODO check if user is allowed to execute command
        try:
            await self.bot.reload_extension(f"Cogs.{cog}")
            logic.logging("info", "bot", "Cog reloaded", {})
            await ctx.reply("Cog reloaded successfully")
        except (ExtensionFailed, ExtensionNotLoaded, ExtensionNotFound, NoEntryPointError):  # TODO differentiate between errors
            logic.logging("warning", "bot", "Cog failed to reload", {})
            await ctx.reply("Cog could not be reloaded")


async def setup(bot) -> None:
    await bot.add_cog(Bot(bot))
