from discord.ext import commands, tasks
from discord.ext.commands import ExtensionFailed, ExtensionNotLoaded, ExtensionNotFound, NoEntryPointError, ExtensionAlreadyLoaded

import datetime as dt
from datetime import time, date

from typing import TYPE_CHECKING
import sqlite3

import lib
from lib import logging, config

if TYPE_CHECKING:
    from discord.ext.commands.context import Context


class Bot(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        logging.extension_success("bot", "Cog initialised", "setup", "Bot")

        self._data_db_save.start()
        logging.default_logger("bot", "DatabaseSavingLoop started", "setup")

    @tasks.loop(time=time(1, tzinfo=dt.UTC))
    async def _data_db_save(self) -> None:
        """Save the database every day at 1am UTC."""
        data_db = sqlite3.connect(config.data_db_path())
        backup_db = sqlite3.connect(f"{config.data_db_backup_path()}{date.today().strftime(config.bot_date_format())}.db")
        data_db.backup(backup_db)

        backup_db.commit()
        backup_db.close()
        data_db.close()

        logging.default_logger("bot", "Database saved", "loop")

    @commands.command()
    async def sync(self, ctx: "Context") -> None:
        """Sync the bot's application commands with discord."""
        if ctx.author.id in config.developer():
            synced = await self.bot.tree.sync()
            logging.sync_commands("command", len(synced), ctx)
            await ctx.reply("Commands synced")

    @commands.command()
    async def reload_cog(self, ctx: "Context", cog: str) -> None:
        """Reload one of the bot's cogs. The cog must be loaded before."""
        if ctx.author.id in config.developer():
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

    @commands.command()
    async def load_cog(self, ctx: "Context", cog: str) -> None:
        """Load one of the bot's cogs. The cog must be unloaded before."""
        if ctx.author.id in config.developer():
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

    @commands.command()
    async def unload_cog(self, ctx: "Context", cog: str) -> None:
        """Unload one of the bot's cogs. The cog must be loaded before."""
        if ctx.author.id in config.developer():
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

    @commands.command()
    async def shutdown(self, ctx: "Context") -> None:
        """# Shut down the bot, this cannot be undone from within Discord"""
        if ctx.author.id in config.developer():
            await ctx.reply("Bot is shutting down")
            await self.bot.close()
            logging.command("bot", "Bot shut down", ctx, "developer", "warn")

    @commands.command()
    async def give_peeps(self, ctx: "Context", amount: str, user_id: str, guild_id: str) -> None:
        """Give peeps to a member effectively bypassing the set probability or cooldowns."""
        # check if command is executed by a developer
        if ctx.author.id in config.developer():
            # Check if all values can be converted to the correct type.
            try:
                amount = int(amount)
            except ValueError:
                logging.invalid_input("peep", "Amount of given peeps is not a number", ctx, "developer", amount)
                await ctx.reply("Amount of peeps is not a number")
                return
            try:
                user_id = int(user_id)
            except ValueError:
                logging.invalid_input("peep", "user_id of member to give peeps to is not a number", ctx, "developer", user_id)
                await ctx.reply("user_id is not a number")
                return
            try:
                guild_id = int(guild_id)
            except ValueError:
                logging.invalid_input("peep", "guild_id of member to give peeps to is not a number", ctx, "developer", guild_id)
                await ctx.reply("guild_id is not a number")
                return

            # check if values are valid
            if amount <= 0:
                await ctx.reply("You need to give at least one peep")
                logging.invalid_input("peep", "Given peeps <= 0", ctx, "developer", amount)
                return

            # Check if the member exists.
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                await ctx.reply("Bot is not in provided guild")
                logging.invalid_input("peep", "bot not in guild of member to give peeps to", ctx, "developer", guild_id)
                return
            member = guild.get_member(user_id)
            if member is None:
                await ctx.reply("Member is not in provided guild")
                logging.invalid_input("peep", "member to give peeps to not in provided guild", ctx, "developer", user_id)
                return

            # add peeps to the member
            lib.sql.add_member(member)
            member_db = lib.sql.get_member(int(guild_id), int(user_id))
            total_peeps = member_db[3]
            received_peeps = member_db[6]

            lib.sql.get_peeps((total_peeps + amount), (received_peeps + amount), guild_id, user_id)

            await ctx.reply("Peeps given to member")
            logging.give_peeps(amount, guild_id, user_id, ctx)

    @commands.command()
    async def remove_peeps(self, ctx: "Context", amount: str, user_id: str, guild_id: str) -> None:
        """Remove peeps from a member."""
        if ctx.author.id in config.developer():
            # Check if all values can be converted to the correct type.
            try:
                amount = int(amount)
            except ValueError:
                logging.invalid_input("peep", "Amount of given removed is not a number", ctx, "developer", amount)
                await ctx.reply("Amount of peeps is not a number")
                return
            try:
                user_id = int(user_id)
            except ValueError:
                logging.invalid_input("peep", "user_id of member to remove peeps from is not a number", ctx, "developer", user_id)
                await ctx.reply("user_id is not a number")
                return
            try:
                guild_id = int(guild_id)
            except ValueError:
                logging.invalid_input("peep", "guild_id of member to remove peeps from is not a number", ctx, "developer", guild_id)
                await ctx.reply("guild_id is not a number")
                return

            # check if values are valid
            if amount <= 0:
                await ctx.reply("You need to remove at least one peep")
                logging.invalid_input("peep", "Removed peeps <= 0", ctx, "developer", amount)

            # Check if the member exists.
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                await ctx.reply("Bot is not in provided guild")
                logging.invalid_input("peep", "bot not in guild of member to give peeps to", ctx, "developer", guild_id)
                return
            member = guild.get_member(user_id)
            if member is None:
                await ctx.reply("Member is not in provided guild")
                logging.invalid_input("peep", "member to give peeps to not in provided guild", ctx, "developer", user_id)
                return

            lib.sql.add_member(member)
            member_db = lib.sql.get_member(guild_id, user_id)
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
