import discord.ext.commands
from discord.ext import commands
from discord.ext.commands import ExtensionFailed, ExtensionNotLoaded, ExtensionNotFound, NoEntryPointError, ExtensionAlreadyLoaded

from typing import TYPE_CHECKING

import logic

if TYPE_CHECKING:
    from discord.ext.commands import Context

class Bot(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def sync(self, ctx: "Context") -> None:
        if ctx.author.id in logic.data["developer"]:
            await self.bot.tree.sync()
            logic.logging("info", "bot", "Commands synced", {})
            await ctx.reply("Commands synced")

    @commands.command()
    async def reload_cog(self, ctx: "Context", cog: str) -> None:
        if ctx.author.id in logic.data["developer"]:
            try:
                await self.bot.reload_extension(f"Cogs.{cog}")
                logic.logging("info", "bot", "Cog reloaded", {
                    "cog": cog
                })
                await ctx.reply("Cog reloaded successfully")
            except ExtensionNotFound:
                await ctx.reply("Cog does not exist")
            except ExtensionNotLoaded:
                await ctx.reply("Cog was not loaded, try load_cog instead")
            except (ExtensionFailed, NoEntryPointError) as exception:
                await ctx.reply("Cog could not be reloaded")
                raise exception

    @commands.command()
    async def load_cog(self, ctx: "Context", cog: str):
        if ctx.author.id in logic.data["developer"]:
            try:
                await self.bot.load_extension(f"Cogs.{cog}")
                logic.logging("info", "bot", "Cog loaded", {
                    "cog": cog
                })
                await ctx.reply("Cog loaded")
            except ExtensionNotFound:
                await ctx.reply("Cog does not exist")
            except ExtensionAlreadyLoaded:
                await ctx.reply("Cog was already loaded")
            except (NoEntryPointError, ExtensionFailed) as exception:
                await ctx.reply("Cog failed to load")
                raise exception

    @commands.command()
    async def unload_cog(self, ctx: "Context", cog: str):
        if ctx.author.id in logic.data["developer"]:
            try:
                await self.bot.unload_extension(f"Cogs.{cog}")
                logic.logging("info", "bot", "Cog unloaded", {
                    "cog": cog
                })
                await ctx.reply("Cog unloaded")
            except ExtensionNotFound:
                await ctx.reply("Cog does not exist")
            except ExtensionNotLoaded:
                await ctx.reply("Cog was already not loaded")


async def setup(bot) -> None:
    await bot.add_cog(Bot(bot))
