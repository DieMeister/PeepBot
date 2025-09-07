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
        backup = sqlite3.connect(f"{lib.get.database_backup_path()}{date.today().strftime(lib.get.date_format())}.db")
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

    @commands.command()
    async def give_peeps(self, ctx: "Context", amount: str, user_id: str, guild_id: str) -> None:
        # FIXME check if command is executed by a developer
        if ctx.author.id in lib.get.developer():
            # Check if all values can be converted to the correct type.
            try:
                amount = int(amount)
            except ValueError:
                logging.invalid_input(Module.PEEP, "Amount of given peeps is not a number", ctx, CommandType.DEVELOPER, amount)
                await ctx.reply("Amount of peeps is not a number")
                return
            try:
                user_id = int(user_id)
            except ValueError:
                logging.invalid_input(Module.PEEP, "user_id of member to give peeps to is not a number", ctx, CommandType.DEVELOPER, user_id)
                await ctx.reply("user_id is not a number")
                return
            try:
                guild_id = int(guild_id)
            except ValueError:
                logging.invalid_input(Module.PEEP, "guild_id of member to give peeps to is not a number", ctx, CommandType.DEVELOPER, guild_id)
                await ctx.reply("guild_id is not a number")
                return

            # check if values are valid
            if amount <= 0:
                await ctx.reply("You need to give at least one peep")
                logging.invalid_input(Module.PEEP, "Given peeps <= 0", ctx, CommandType.DEVELOPER, amount)

            # Check if the member exists.
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                await ctx.reply("Bot is not in provided guild")
                logging.invalid_input(Module.PEEP, "bot not in guild of member to give peeps to", ctx, CommandType.DEVELOPER, guild_id)
                return
            member = guild.get_member(user_id)
            if member is None:
                await ctx.reply("Member is not in provided guild")
                logging.invalid_input(Module.PEEP, "member to give peeps to not in provided guild", ctx, CommandType.DEVELOPER, user_id)
                return

            # add peeps to the member
            lib.sql.add_member(member)
            member_db = lib.sql.get_member(int(guild_id), int(user_id))
            total_peeps = member_db[3]
            received_peeps = member_db[7]
            data_db = sqlite3.connect(lib.get.database_path())
            data_db.execute("""
            UPDATE members
            SET 
                caught_peeps = ?,
                received_peeps = ?
            WHERE guild_id = ?
            AND user_id = ?
            """, ((total_peeps + amount), (received_peeps + amount), guild_id, user_id))
            data_db.commit()
            data_db.close()
            await ctx.reply("Peeps given to member")
            logging.give_peeps(amount, guild_id, user_id, ctx)

    @commands.command()
    async def remove_peeps(self, ctx: "Context", amount: str, user_id: str, guild_id: str) -> None:
        """Remove peeps from a member."""
        if ctx.author.id in lib.get.developer():
            # Check if all values can be converted to the correct type.
            try:
                amount = int(amount)
            except ValueError:
                logging.invalid_input(Module.PEEP, "Amount of given removed is not a number", ctx, CommandType.DEVELOPER, amount)
                await ctx.reply("Amount of peeps is not a number")
                return
            try:
                user_id = int(user_id)
            except ValueError:
                logging.invalid_input(Module.PEEP, "user_id of member to remove peeps from is not a number", ctx, CommandType.DEVELOPER, user_id)
                await ctx.reply("user_id is not a number")
                return
            try:
                guild_id = int(guild_id)
            except ValueError:
                logging.invalid_input(Module.PEEP, "guild_id of member to remove peeps from is not a number", ctx, CommandType.DEVELOPER, guild_id)
                await ctx.reply("guild_id is not a number")
                return

            # check if values are valid
            if amount <= 0:
                await ctx.reply("You need to remove at least one peep")
                logging.invalid_input(Module.PEEP, "Removed peeps <= 0", ctx, CommandType.DEVELOPER, amount)

            # Check if the member exists.
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                await ctx.reply("Bot is not in provided guild")
                logging.invalid_input(Module.PEEP, "bot not in guild of member to give peeps to", ctx, CommandType.DEVELOPER, guild_id)
                return
            member = guild.get_member(user_id)
            if member is None:
                await ctx.reply("Member is not in provided guild")
                logging.invalid_input(Module.PEEP, "member to give peeps to not in provided guild", ctx, CommandType.DEVELOPER, user_id)
                return

            lib.sql.add_member(member)
            member_db = lib.sql.get_member(member.guild_id, user_id)
            total_peeps = member_db[3]
            # check if member has enough peeps to remove the given amount.
            if (total_peeps - amount) < 0:
                new_peeps = 0
                await ctx.reply("Member has less peeps than the provided amount, they are set to 0 instead.")
            else:
                new_peeps = total_peeps - amount
                await ctx.reply("Peeps removed from member.")
            # remove peeps from member
            lib.sql.remove_peeps(new_peeps, guild_id, user_id)
            logging.remove_peeps(total_peeps, amount, guild_id, user_id, ctx)


async def setup(bot) -> None:
    await bot.add_cog(Bot(bot))
