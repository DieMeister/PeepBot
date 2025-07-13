import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import ExtensionFailed, ExtensionNotLoaded, ExtensionNotFound, NoEntryPointError, ExtensionAlreadyLoaded

import datetime
from datetime import datetime as dt, time, date

import logic
from lib.date_time import get_datetime_string

from typing import TYPE_CHECKING
import sqlite3

if TYPE_CHECKING:
    from discord.ext.commands import Context
    from discord import Guild, Member, Interaction


class Bot(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        logic.logging("info", "bot", "Cog initialised", {
            "cog_name": "Bot",
            "command": False
        })
        self.database_save.start()
        logic.logging("info", "bot", "DatabaseSavingLoop started", {
            "command": False
        })

    # FIXME figure out how to copy the database
    @tasks.loop(time=time(1, tzinfo=datetime.UTC))
    async def database_save(self):
        database = sqlite3.connect(logic.config["file_paths"]["database"])
        backup = sqlite3.connect(f"{logic.config['file_paths']['database_saves']}{date.today().strftime(logic.config['datetime_formats']['date'])}.json")
        database.backup(backup)

        backup.commit()
        backup.close()
        database.close()

        logic.logging("info", "bot", "Database saved", {
            "command": False
        })

    @commands.Cog.listener()
    async def on_guild_join(self, guild: "Guild"):
        connection = sqlite3.connect(logic.config["file_paths"]["database"])

        # checks if guild is already in database
        known_guild = connection.execute("""
        SELECT *
        FROM guilds
        WHERE guild_id = ?
        """, (guild.id,)).fetchone()
        if known_guild:
            # FIXME add missing members
            return

        connection.execute("""
        INSERT INTO guilds (guild_id, last_peep)
        VALUES (?, ?)
        """, (guild.id, get_datetime_string(dt.now(datetime.UTC))))
        connection.commit()

        members = []
        for member in guild.members:
            members.append(
                (
                    member.id,
                    guild.id,
                    get_datetime_string(dt.now(datetime.UTC))
                )
            )
        connection.executemany("""
        INSERT INTO members (
            user_id,
            guild_id,
            last_peep
        )
        VALUES (?, ?, ?)
        """, members)
        connection.commit()

        logic.logging("info", "bot", "Bot joined Guild", {
            "guild_id": guild.id,
            "guild_name": guild.name,
            "command": False
        })

        connection.close()


    @commands.Cog.listener()
    async def on_member_join(self, member: "Member"):
        connection = sqlite3.connect(logic.config["file_paths"]["database"])

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
        """, (member.id, member.guild.id, get_datetime_string(dt.now(datetime.UTC))))
        connection.commit()

        logic.logging("info", "bot", "Member joined Guild", {
            "guild_id": member.guild.id,
            "user_id": member.id,
            "user_name": member.name,
            "command": False
        })
        connection.close()


    # Sync all application commands with Discord
    @commands.command()
    async def sync(self, ctx: "Context") -> None:
        if logic.is_developer(ctx.author.id):
            synced = await self.bot.tree.sync()
            logic.logging("info", "bot", "Commands synced", {
                "amount": len(synced),
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "DeveloperCommand",
                    "parameters": None
                }
            })
            await ctx.reply("Commands synced")

    # Reload a currently loaded extension
    @commands.command()
    async def reload_cog(self, ctx: "Context", cog: str) -> None:
        if logic.is_developer(ctx.author.id):
            try:
                await self.bot.reload_extension(f"Cogs.{cog}")
                logic.logging("info", "bot", "Cog reloaded", {
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "DeveloperCommand",
                        "parameters": {
                            "extension": cog
                        }
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
                    "reason": "Extension has no entry point",
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "DeveloperCommand",
                        "parameters": {
                            "extension": cog
                        }
                    }
                })
            except ExtensionFailed:
                await ctx.reply("Cog failed to load")
                logic.logging("error", "bot", "Extension failed to load", {
                    "reason": "no further information",
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "DeveloperCommand",
                        "parameters": {
                            "extension": cog
                        }
                    }
                })

    # Load a currently unloaded extension
    @commands.command()
    async def load_cog(self, ctx: "Context", cog: str):
        if logic.is_developer(ctx.author.id):
            try:
                await self.bot.load_extension(f"Cogs.{cog}")
                logic.logging("info", "bot", "Cog loaded", {
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "DeveloperCommand",
                        "parameters": {
                            "extension": cog
                        }
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
                    "reason": "Extension has no entry point",
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "DeveloperCommand",
                        "parameters": {
                            "extension": cog
                        }
                    }
                })
            except ExtensionFailed:
                await ctx.reply("Cog failed to load")
                logic.logging("error", "bot", "Extension failed to load", {
                    "reason": "no further information",
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "DeveloperCommand",
                        "parameters": {
                            "extension": cog
                        }
                    }
                })

    # Unload a currently loaded extension
    @commands.command()
    async def unload_cog(self, ctx: "Context", cog: str):
        if logic.is_developer(ctx.author.id):
            try:
                await self.bot.unload_extension(f"Cogs.{cog}")
                logic.logging("info", "bot", "Cog unloaded", {
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "DeveloperCommand",
                        "parameters": {
                            "extension": cog
                        }
                    }
                })
                await ctx.reply("Cog unloaded")
            except ExtensionNotFound:
                await ctx.reply("Cog does not exist")
            except ExtensionNotLoaded:
                await ctx.reply("Cog was already not loaded")

    # Shut down the bot, this cannot be undone from within Discord
    @commands.command()
    async def shutdown(self, ctx: "Context"):
        if logic.is_developer(ctx.author.id):
            await ctx.reply("Bot is shutting down")
            await self.bot.close()
            logic.logging("info", "bot", "Bot closed", {
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "DeveloperCommand",
                    "parameters": None
                }
            })

    # Send an embed explaining the DeveloperCommands
    @commands.command()
    async def devhelp(self, ctx: "Context"):
        if logic.is_developer(ctx.author.id):
            embed = discord.Embed(color=logic.config["embed_color"],
                                  title="Developer Help",
                                  description="Explains every DeveloperCommand",
                                  timestamp=dt(2025, 6, 16, 11, 7, tzinfo=datetime.UTC))
            embed.set_footer(text="Bot")
            embed.add_field(name="reload_cog <Cog>", value="Reloads a provided Cog. Existing Cogs are:\n- Bot\n- Peep\n- Config\n- EasterEgg", inline=True)
            embed.add_field(name="unload_cog <Cog>", value="Unloads a before loaded Cog (the same as `reload_cog` can access).\n**WARNING:** once Bot is unloaded it can not be loaded again, use `reload_cog` instead.")
            embed.add_field(name="load_cog <Cog>", value="Loads a before unloaded Cog (the same as `reload_cog` can access).")
            embed.add_field(name="sync", value="Syncs every application command with discord. Needs to be done whenever a command is changed in the source code.", inline=True)
            embed.add_field(name="shutdown", value="shuts down the bot causing it to stop running. This should only be the last escalation step since it is not possible to restart it from within Discord.", inline=True)
            embed.add_field(name="help", value="shows this message.")
            embed.add_field(name="More Help", value="If this didn't explain the question feel free to dm `@diemeister`", inline=False)

            await ctx.reply(embed=embed)
            logic.logging("info", "bot", "DeveloperHelpEmbed sent", {
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "DeveloperCommand",
                    "parameters": None
                }
            })
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
    async def help(self, interaction: "Interaction", problem: app_commands.Choice[str]):
        if problem.value == "setup":
            embed = discord.Embed(
                color=logic.config["embed_color"],
                title="Setup Help",
                description="Everything you need to do to make the bot working",
                timestamp=dt(2025, 6, 22, 21, 20, tzinfo=datetime.UTC)
            )
            embed.add_field(name="/add_channel <channel>", value="adds a channel as allowed channel. The !psps command works only in allowed channels, everywhere else it will not send a response.")
            embed.add_field(name="/remove_channel <channel>", value="removes a channel as allowed channel. This leads to !psps commands not getting a response anymore.")
            embed.add_field(name="/change_peep_message <message_type> <message>", value="changes the response the bot gives when executing !psps. `message_type` determines which message will be changed, and `message`is the actual response the bot sends.\nNote that the bot automatically adds 'You have {number of peeps} peeps now' after the `You got a peep` message. This can not be turned off.")
            embed.set_footer(text="Bot")
            logic.logging("info", "bot", "Member executed /help", {
                "command": {
                    "guild": interaction.guild.id,
                    "channel": interaction.channel.id,
                    "user": interaction.user.id,
                    "type": "DeveloperCommand",
                    "parameters": {
                        "problem": problem.value
                    }
                }
            })
        elif problem.value == "usage":
            embed = discord.Embed(
                color=logic.config["embed_color"],
                title="Usage Help",
                timestamp=dt(2025, 6, 22, 21, 20, tzinfo=datetime.UTC)
            )
            embed.add_field(name="psps", value="To get peeps type `!psps` in an allowed chat, if you don't know which chats are allowed ask your server manager, admin, or owner. If you are the person responsible to set up the bot please execute /help <setup>\nYou have to wait 10 minutes before you can execute the command again.\nYou have to wait 1 minute after someone else executed the command before you can execute it.")
            embed.set_footer(text="Bot")
            logic.logging("info", "bot", "Member executed /help", {
                "command": {
                    "guild": interaction.guild.id,
                    "channel": interaction.channel.id,
                    "user": interaction.user.id,
                    "type": "DeveloperCommand",
                    "parameters": {
                        "problem": problem.value
                    }
                }
            })
        else:
            embed = discord.Embed(
                color=logic.config["embed_color"],
                title="Error",
                description="Something went wrong, please try again or contact `@diemeister`",
                timestamp=dt(2025, 6, 22, 21, 20, tzinfo=datetime.UTC)
            )
            logic.logging("warn", "bot", "Member executed /help", {
                "error": "`problem.value` different from possible values",
                "command": {
                    "guild": interaction.guild.id,
                    "channel": interaction.channel.id,
                    "user": interaction.user.id,
                    "type": "DeveloperCommand",
                    "parameters": {
                        "problem": problem.value
                    }
                }
            })
        await interaction.response.send_message(embed=embed)

        # TODO Leaderboard
        # TODO Show amount of peeps


async def setup(bot) -> None:
    await bot.add_cog(Bot(bot))
