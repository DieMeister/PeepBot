from typing import TYPE_CHECKING

from discord.ext import commands
from discord.ext.commands import ExtensionFailed, ExtensionNotLoaded, ExtensionNotFound, NoEntryPointError, ExtensionAlreadyLoaded

import logic

if TYPE_CHECKING:
    from discord.ext.commands import Context


class Bot(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Sync all application commands with Discord
    @commands.command()
    async def sync(self, ctx: "Context") -> None:
        if ctx.author.id in logic.data["developer"]:
            await self.bot.tree.sync()
            logic.logging("info", "bot", "Commands synced", {
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "DeveloperCommand"
                }
            })
            await ctx.reply("Commands synced")

    @commands.command()
    async def reload_cog(self, ctx: "Context", cog: str) -> None:
        """Reload a currently loaded extension.

        Parameters
        ----------
        ctx:
            the context provided by discord
        cog:
            the extension's name that is reloaded

        Raises
        ------
        ExtensionNotFound
            the provided extension does not exist
        ExtensionNotLoaded
            the provided extension was not loaded in the first place
        NoEntryPointError
            raised when the extension has no setup function
        ExtensionFailed
            raised when the extension failed to reload
        """
        if ctx.author.id in logic.data["developer"]:
            try:
                await self.bot.reload_extension(f"Cogs.{cog}")
                logic.logging("info", "bot", "Cog reloaded", {
                    "cog": cog,
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "DeveloperCommand"
                    }
                })
                await ctx.reply("Cog reloaded successfully")
            except ExtensionNotFound:
                await ctx.reply("Cog does not exist")
            except ExtensionNotLoaded:
                await ctx.reply("Cog was not loaded before, try load_cog instead")
            except (ExtensionFailed, NoEntryPointError) as exception:
                await ctx.reply("Cog could not be reloaded")
                raise exception

    @commands.command()
    async def load_cog(self, ctx: "Context", cog: str):
        """Load a currently unloaded extension.

        Parameters
        ----------
        ctx:
            the command's context provided by discord
        cog:
            the extension's name that is being loaded

        Raises
        ------
        ExtensionNotFound
            the extension does not exist
        ExtensionAlreadyLoaded
            the extension is already loaded
        NoEntryPointError
            raised when the extension has no setup function
        ExtensionFailed
            raised when the extension failed to load
        """
        if ctx.author.id in logic.data["developer"]:
            try:
                await self.bot.load_extension(f"Cogs.{cog}")
                logic.logging("info", "bot", "Cog loaded", {
                    "cog": cog,
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "DeveloperCommand"
                    }
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
        """Unload a currently loaded extension.

        Parameters
        ----------
        ctx:
            the command's context provided by discord
        cog:
            the extension's name that is being unloaded

        Raises
        ------
        ExtensionNotFound
            the extension does not exist
        ExtensionNotLoaded
            the extension was not loaded in the first place
        """
        if ctx.author.id in logic.data["developer"]:
            try:
                await self.bot.unload_extension(f"Cogs.{cog}")
                logic.logging("info", "bot", "Cog unloaded", {
                    "cog": cog,
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "DeveloperCommand"
                    }
                })
                await ctx.reply("Cog unloaded")
            except ExtensionNotFound:
                await ctx.reply("Cog does not exist")
            except ExtensionNotLoaded:
                await ctx.reply("Cog was already not loaded")

    # TODO !shutdown command
    @commands.command()
    async def shutdown(self, ctx: "Context"):
        if ctx.author.id in logic.data["developer"]:
            self.bot.close()
            logic.logging("info", "bot", "Bot closed", {
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "DeveloperCommand"
                }
            })

    # TODO !help command
    # TODO /help command


async def setup(bot) -> None:
    await bot.add_cog(Bot(bot))
