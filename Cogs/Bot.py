from discord.ext import commands, tasks
from discord.ext.commands import ExtensionFailed, ExtensionNotLoaded, ExtensionNotFound, NoEntryPointError, ExtensionAlreadyLoaded

import datetime as dt
from datetime import time, date

from typing import TYPE_CHECKING
import sqlite3

import lib
from lib import logging
from lib.logging import Module, ExecutionMethod, LogType, CommandType

if TYPE_CHECKING:
    from discord.ext.commands.context import Context


class Bot(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        logging.extension_success(Module.BOT, "Cog initialised", ExecutionMethod.SETUP, "Bot")

        self.database_save.start()
        logging.default_logger(Module.BOT, "DatabaseSavingLoop started", ExecutionMethod.SETUP)

    @tasks.loop(time=time(1, tzinfo=dt.UTC))
    async def database_save(self) -> None:
        database = sqlite3.connect(lib.get.database_path())
        backup = sqlite3.connect(f"{lib.get.database_backup_path()}{date.today().strftime(lib.get.date_format())}.json")
        database.backup(backup)

        backup.commit()
        backup.close()
        database.close()

        logging.default_logger(Module.BOT, "Database saved", ExecutionMethod.LOOP)


    # Sync all application commands with Discord
    @commands.command()
    async def sync(self, ctx: "Context") -> None:
        if ctx.author.id in lib.get.developer():
            synced = await self.bot.tree.sync()
            logging.sync_commands(ExecutionMethod.COMMAND, len(synced), ctx)
            await ctx.reply("Commands synced")

    # Reload a currently loaded extension
    @commands.command()
    async def reload_cog(self, ctx: "Context", cog: str) -> None:
        if ctx.author.id in lib.get.developer():
            try:
                await self.bot.reload_extension(f"Cogs.{cog}")
                logging.extension_success(Module.BOT, "Cog reloaded successfully", ExecutionMethod.COMMAND, cog, ctx)
                await ctx.reply("Cog reloaded successfully")
            except ExtensionNotFound:
                await ctx.reply("Cog does not exist")
                logging.extension_error("Extension failed to reload", ExecutionMethod.COMMAND, cog, "Cog does not exist", ctx, LogType.WARN)
            except ExtensionNotLoaded:
                await ctx.reply("Cog was not loaded before, try load_cog instead")
            except NoEntryPointError:
                await ctx.reply("Cog has no entry point")
                logging.extension_error("Extension failed to reload", ExecutionMethod.COMMAND, cog, "Extension has no EntryPoint", ctx)
            except ExtensionFailed:
                await ctx.reply("Cog failed to load")
                logging.extension_error("Extension failed to reload", ExecutionMethod.COMMAND, cog, "No further information", ctx)

    # Load a currently unloaded extension
    @commands.command()
    async def load_cog(self, ctx: "Context", cog: str) -> None:
        if ctx.author.id in lib.get.developer():
            try:
                await self.bot.load_extension(f"Cogs.{cog}")
                logging.extension_success(Module.BOT, "Cog loaded successfully", ExecutionMethod.COMMAND, cog, ctx)
                await ctx.reply("Cog loaded")
            except ExtensionNotFound:
                await ctx.reply("Cog does not exist")
                logging.extension_error("Extension failed to load", ExecutionMethod.COMMAND, cog, "Cog does not exist", ctx, LogType.WARN)
            except ExtensionAlreadyLoaded:
                await ctx.reply("Cog was already loaded")
                logging.extension_error("Extension failed to load", ExecutionMethod.COMMAND, cog, "Cog was already loaded", ctx, LogType.WARN)
            except NoEntryPointError:
                await ctx.reply("Cog has no entry point")
                logging.extension_error("Extension failed to load", ExecutionMethod.COMMAND, cog, "Extension has no EntryPoint", ctx)
            except ExtensionFailed:
                await ctx.reply("Cog failed to load")
                logging.extension_error("Extension failed to load", ExecutionMethod.COMMAND, cog, "no further information", ctx)

    # Unload a currently loaded extension
    @commands.command()
    async def unload_cog(self, ctx: "Context", cog: str) -> None:
        if ctx.author.id in lib.get.developer():
            try:
                await self.bot.unload_extension(f"Cogs.{cog}")
                logging.extension_success(Module.BOT, "Extension loaded successfully", ExecutionMethod.COMMAND, cog, ctx)
                await ctx.reply("Cog unloaded")
            except ExtensionNotFound:
                await ctx.reply("Cog does not exist")
                logging.extension_error("Extension failed to unload", ExecutionMethod.COMMAND, cog, "Cog does not exist", ctx, LogType.WARN)
            except ExtensionNotLoaded:
                await ctx.reply("Cog was already not loaded")
                logging.extension_error("Extension failed to unload", ExecutionMethod.COMMAND, cog, "Cog was already not loaded", ctx, LogType.WARN)

    # Shut down the bot, this cannot be undone from within Discord
    @commands.command()
    async def shutdown(self, ctx: "Context") -> None:
        if ctx.author.id in lib.get.developer():
            await ctx.reply("Bot is shutting down")
            await self.bot.close()
            logging.command(Module.BOT, "Bot shut down", ctx, CommandType.DEVELOPER, LogType.WARN)


    # TODO cleanup command


async def setup(bot) -> None:
    await bot.add_cog(Bot(bot))
