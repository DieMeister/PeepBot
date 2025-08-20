from discord.ext import commands, tasks
from discord.ext.commands import ExtensionFailed, ExtensionNotLoaded, ExtensionNotFound, NoEntryPointError, ExtensionAlreadyLoaded

import datetime as dt
from datetime import datetime, time, date

from typing import TYPE_CHECKING
import sqlite3

import lib
from lib import logging, get

if TYPE_CHECKING:
    from discord.ext.commands.context import Context
    from discord import Guild, Member


class Bot(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        logging.extension_success("bot", "Cog initialised", "setup", "Bot")

        self.database_save.start()
        logging.default_logger("bot", "DatabaseSavingLoop started", "setup")

    @tasks.loop(time=time(1, tzinfo=dt.UTC))
    async def database_save(self) -> None:
        database = sqlite3.connect(lib.get.database_path())
        backup = sqlite3.connect(f"{lib.get.database_backup_path()}{date.today().strftime(lib.get.date_format())}.json")
        database.backup(backup)

        backup.commit()
        backup.close()
        database.close()

        logging.default_logger("bot", "Database saved", "loop")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: "Guild") -> None:
        timestamp = datetime.now(dt.UTC)
        timestamp_str = get.dt_string(timestamp)
        members = []

        if lib.sql.get_guild(guild.id):
            for member in guild.members:
                if not lib.sql.get_member(guild.id, member.id):
                    members.append(
                        (
                            member.id,
                            guild.id,
                            timestamp_str
                        )
                    )
            members_added = lib.sql.add_members(members)
        else:
            members_added = lib.sql.add_guild(guild, timestamp)

        logging.guild_join(guild, members_added)

    @commands.Cog.listener()
    async def on_member_join(self, member: "Member") -> None:
        if not lib.sql.get_member(member.guild.id, member.id):
            lib.sql.add_member(member.id, member.guild.id, datetime.now(dt.UTC))
        logging.member_join(member)


    # Sync all application commands with Discord
    @commands.command()
    async def sync(self, ctx: "Context") -> None:
        if ctx.author.id in lib.get.developer():
            synced = await self.bot.tree.sync()
            logging.sync_commands("command", len(synced), ctx)
            await ctx.reply("Commands synced")

    # Reload a currently loaded extension
    @commands.command()
    async def reload_cog(self, ctx: "Context", cog: str) -> None:
        if ctx.author.id in lib.get.developer():
            try:
                await self.bot.reload_extension(f"Cogs.{cog}")
                logging.extension_success("bot", "Cog reloaded successfully", "command", cog, ctx)
                await ctx.reply("Cog reloaded successfully")
            except ExtensionNotFound:
                await ctx.reply("Cog does not exist")
                logging.extension_error("Extension failed to reload", "command", cog, "Cog does not exist", ctx, "warn")
            except ExtensionNotLoaded:
                await ctx.reply("Cog was not loaded before, try load_cog instead")
            except NoEntryPointError:
                await ctx.reply("Cog has no entry point")
                logging.extension_error("Extension failed to reload", "command", cog, "Extension has no EntryPoint", ctx)
            except ExtensionFailed:
                await ctx.reply("Cog failed to load")
                logging.extension_error("Extension failed to reload", "command", cog, "No further information", ctx)

    # Load a currently unloaded extension
    @commands.command()
    async def load_cog(self, ctx: "Context", cog: str) -> None:
        if ctx.author.id in lib.get.developer():
            try:
                await self.bot.load_extension(f"Cogs.{cog}")
                logging.extension_success("bot", "Cog loaded successfully", "command", cog, ctx)
                await ctx.reply("Cog loaded")
            except ExtensionNotFound:
                await ctx.reply("Cog does not exist")
                logging.extension_error("Extension failed to load", "command", cog, "Cog does not exist", ctx, "warn")
            except ExtensionAlreadyLoaded:
                await ctx.reply("Cog was already loaded")
                logging.extension_error("Extension failed to load", "command", cog, "Cog was already loaded", ctx, "warn")
            except NoEntryPointError:
                await ctx.reply("Cog has no entry point")
                logging.extension_error("Extension failed to load", "command", cog, "Extension has no EntryPoint", ctx)
            except ExtensionFailed:
                await ctx.reply("Cog failed to load")
                logging.extension_error("Extension failed to load", "command", cog, "no further information", ctx)

    # Unload a currently loaded extension
    @commands.command()
    async def unload_cog(self, ctx: "Context", cog: str) -> None:
        if ctx.author.id in lib.get.developer():
            try:
                await self.bot.unload_extension(f"Cogs.{cog}")
                logging.extension_success("bot", "Extension loaded successfully", "command", cog, ctx)
                await ctx.reply("Cog unloaded")
            except ExtensionNotFound:
                await ctx.reply("Cog does not exist")
                logging.extension_error("Extension failed to unload", "command", cog, "Cog does not exist", ctx, "warn")
            except ExtensionNotLoaded:
                await ctx.reply("Cog was already not loaded")
                logging.extension_error("Extension failed to unload", "command", cog, "Cog was already not loaded", ctx, "warn")

    # Shut down the bot, this cannot be undone from within Discord
    @commands.command()
    async def shutdown(self, ctx: "Context") -> None:
        if ctx.author.id in lib.get.developer():
            await ctx.reply("Bot is shutting down")
            await self.bot.close()
            logging.command("bot", "Bot shut down", ctx, "developer", "warn")



    # TODO cleanup command


async def setup(bot) -> None:
    await bot.add_cog(Bot(bot))
