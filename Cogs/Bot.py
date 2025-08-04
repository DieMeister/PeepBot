import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import ExtensionFailed, ExtensionNotLoaded, ExtensionNotFound, NoEntryPointError, ExtensionAlreadyLoaded

import datetime as dt
from datetime import datetime, time, date

from typing import TYPE_CHECKING
import sqlite3

import lib
from lib import logging, get_datetime_string, is_member_in_database

if TYPE_CHECKING:
    from discord.ext.commands.context import Context
    from discord import Guild, Member, Interaction


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
        timestamp_str = get_datetime_string(timestamp)
        members = []
        con = sqlite3.connect(lib.get.database_path())

        # checks if guild is already in database
        known_guild = con.execute("""
        SELECT *
        FROM guilds
        WHERE guild_id = ?
        """, (guild.id,)).fetchone()
        con.close()

        if known_guild is None:
            lib.sql.add_guild(guild.id, timestamp)
            for member in guild.members:
                members.append(
                    (
                        member.id,
                        guild.id,
                        timestamp_str
                    )
                )
        else:
            for member in guild.members:
                if not is_member_in_database(guild.id, member.id):
                    members.append(
                        (
                            member.id,
                            guild.id,
                            timestamp_str
                        )
                    )

        members_added = lib.sql.add_members(members)
        logging.guild_join(guild, members_added)

    @commands.Cog.listener()
    async def on_member_join(self, member: "Member") -> None:
        connection = sqlite3.connect(lib.get.database_path())

        known_member = connection.execute("""
        SELECT *
        FROM guilds
        WHERE user_id = ?
        AND guild_id = ?
        """, (member.id, member.guild.id)).fetchone()
        if known_member:
            return

        connection.execute("""
        INSERT INTO members (user_id, guild_id, last_peep)
        VALUES (?, ?, ?)
        """, (member.id, member.guild.id, get_datetime_string(datetime.now(dt.UTC))))
        connection.commit()
        logging.member_join(member)
        connection.close()

    # Sync all application commands with Discord
    @commands.command()
    async def sync(self, ctx: "Context") -> None:
        if lib.is_developer(ctx.author.id):
            synced = await self.bot.tree.sync()
            logging.sync_commands("command", len(synced), ctx)
            await ctx.reply("Commands synced")

    # Reload a currently loaded extension
    @commands.command()
    async def reload_cog(self, ctx: "Context", cog: str) -> None:
        if lib.is_developer(ctx.author.id):
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
        if lib.is_developer(ctx.author.id):
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
        if lib.is_developer(ctx.author.id):
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
        if lib.is_developer(ctx.author.id):
            await ctx.reply("Bot is shutting down")
            await self.bot.close()
            logging.command("bot", "Bot shut down", ctx, "developer", "warn")

    # FIXME update embed
    # Send an embed explaining the DeveloperCommands
    @commands.command()
    async def devhelp(self, ctx: "Context") -> None:
        if lib.is_developer(ctx.author.id):
            embed = discord.Embed(color=lib.get.embed_color(),
                                  title="Developer Help",
                                  description="Explains every DeveloperCommand",
                                  timestamp=datetime(2025, 6, 16, 11, 7, tzinfo=dt.UTC))
            embed.set_footer(text="Bot")
            embed.add_field(name="reload_cog <Cog>", value="Reloads a provided Cog. Existing Cogs are:\n- Bot\n- Peep\n- Config\n- EasterEgg", inline=True)
            embed.add_field(name="unload_cog <Cog>", value="Unloads a before loaded Cog (the same as `reload_cog` can access).\n**WARNING:** once Bot is unloaded it can not be loaded again, use `reload_cog` instead.")
            embed.add_field(name="load_cog <Cog>", value="Loads a before unloaded Cog (the same as `reload_cog` can access).")
            embed.add_field(name="sync", value="Syncs every application command with discord. Needs to be done whenever a command is changed in the source code.", inline=True)
            embed.add_field(name="shutdown", value="shuts down the bot causing it to stop running. This should only be the last escalation step since it is not possible to restart it from within Discord.", inline=True)
            embed.add_field(name="help", value="shows this message.")
            embed.add_field(name="More Help", value="If this didn't explain the question feel free to dm `@diemeister`", inline=False)

            await ctx.reply(embed=embed)
            logging.help_embed("dev", ctx, "developer")
        else:
            await ctx.reply("This bot supports application (/) commands, please use `/help`")

    @app_commands.command(name="help", description="provides help for usage and setup of the bot")
    @app_commands.describe(
        problem="The problem you need help with"
    )
    @app_commands.choices(
        problem=[
            app_commands.Choice(name="Setup", value="setup"),
            app_commands.Choice(name="Usage", value="usage")
        ]
    )
    async def help(self, interaction: "Interaction", problem: app_commands.Choice[str]) -> None:
        if problem.value == "setup":
            embed = discord.Embed(
                color=lib.get.embed_color(),
                title="Setup Help",
                description="Everything you need to do to make the bot working",
                timestamp=datetime(2025, 6, 22, 21, 20, tzinfo=dt.UTC)
            )
            embed.add_field(name="/add_channel <channel>", value="adds a channel as allowed channel. The !psps command works only in allowed channels, everywhere else it will not send a response.")
            embed.add_field(name="/remove_channel <channel>", value="removes a channel as allowed channel. This leads to !psps commands not getting a response anymore.")
            embed.add_field(name="/change_peep_message <message_type> <message>", value="changes the response the bot gives when executing !psps. `message_type` determines which message will be changed, and `message`is the actual response the bot sends.\nNote that the bot automatically adds 'You have {number of peeps} peeps now' after the `You got a peep` message. This can not be turned off.")
            embed.set_footer(text="Bot")

            logging.help_embed("setup", interaction, "member")
        elif problem.value == "usage":
            embed = discord.Embed(
                color=lib.get.embed_color(),
                title="Usage Help",
                timestamp=datetime(2025, 6, 22, 21, 20, tzinfo=dt.UTC)
            )
            embed.add_field(name="psps", value="To get peeps type `!psps` in an allowed chat, if you don't know which chats are allowed ask your server manager, admin, or owner. If you are the person responsible to set up the bot please execute /help <setup>\nYou have to wait 10 minutes before you can execute the command again.\nYou have to wait 1 minute after someone else executed the command before you can execute it.")
            embed.set_footer(text="Bot")

            logging.help_embed("usage", interaction, "member")
        else:
            raise ValueError("HelpEmbedType does not match")

        await interaction.response.send_message(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Bot(bot))
