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

    # Reload a currently loaded extension
    @commands.command()
    async def reload_cog(self, ctx: "Context", cog: str) -> None:
        if ctx.author.id in logic.data["developer"]:
            try:
                await self.bot.reload_extension(f"Cogs.{cog}")
                logic.logging("info", "bot", "Cog reloaded", {
                    "extension": cog,
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
            except NoEntryPointError:
                await ctx.reply("Cog has no entry point")
                logic.logging("error", "bot", "Extension failed to load", {
                    "extension": cog,
                    "reason": "Extension has no entry point",
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "DeveloperCommand"
                    }
                })
            except ExtensionFailed:
                await ctx.reply("Cog failed to load")
                logic.logging("error", "bot", "Extension failed to load", {
                    "extension": cog,
                    "reason": "no further information",
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "DeveloperCommand"
                    }
                })

    # Load a currently unloaded extension
    @commands.command()
    async def load_cog(self, ctx: "Context", cog: str):
        if ctx.author.id in logic.data["developer"]:
            try:
                await self.bot.load_extension(f"Cogs.{cog}")
                logic.logging("info", "bot", "Cog loaded", {
                    "extension": cog,
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
            except NoEntryPointError:
                await ctx.reply("Cog has no entry point")
                logic.logging("error", "bot", "Extension failed to load", {
                    "extension": cog,
                    "reason": "Extension has no entry point",
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "DeveloperCommand"
                    }
                })
            except ExtensionFailed:
                await ctx.reply("Cog failed to load")
                logic.logging("error", "bot", "Extension failed to load", {
                    "extension": cog,
                    "reason": "no further information",
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "DeveloperCommand"
                    }
                })

    # Unload a currently loaded extension
    @commands.command()
    async def unload_cog(self, ctx: "Context", cog: str):
        if ctx.author.id in logic.data["developer"]:
            try:
                await self.bot.unload_extension(f"Cogs.{cog}")
                logic.logging("info", "bot", "Cog unloaded", {
                    "extension": cog,
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
