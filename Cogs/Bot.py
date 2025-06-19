import discord
from discord.ext import commands
from discord.ext.commands import ExtensionFailed, ExtensionNotLoaded, ExtensionNotFound, NoEntryPointError, ExtensionAlreadyLoaded

import datetime
from datetime import datetime as dt

from typing import TYPE_CHECKING

import logic

if TYPE_CHECKING:
    from discord.ext.commands import Context
    from discord import Guild, Member


class Bot(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: "Guild"):
        if logic.get_item(logic.data["guilds"], "guild_id", guild.id) is None:
            return

        entry = {
            "guild_id": guild.id,
            "last_peep": "2025-01-01T00:00:00",
            "peep_success_massage": "You got a peep :)",
            "peep_scratch_massage": "You got scratched :(",
            "peep_no_peep_message": "No peep, L",
            "allowed_channel_ids": [],
            "members": []
        }
        for member in guild.members:
            entry["members"].append({
                "user_id": member.id,
                "peep_count": 0,
                "execute_psps_timestamp": "2025-01-01T00:00:00"
            })
        logic.data["guilds"].append(entry)
        logic.logging("info", "bot", "Bot joined Guild", {
            "guild_id": guild.id,
            "guild_name": guild.name,
            "command": False
        })
        logic.save_data(logic.data, logic.database_path)


    @commands.Cog.listener()
    async def on_member_join(self, member: "Member"):
        guild = logic.get_item(logic.data["guilds"], "guild_id", member.guild.id)
        if logic.get_item(guild["members"], "user_id", member.id) is None:
            return

        guild["members"].append({
            "user_id": member.id,
            "peep_count": 0,
            "execute_psps_timestamp": "2025-01-01T00:00:00"
        })
        logic.logging("info", "bot", "Member joined Guild", {
            "guild_id": member.guild.id,
            "user_id": member.id,
            "user_name": member.name,
            "command": False
        })
        logic.save_data(logic.data, logic.database_path)


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
                    "type": "DeveloperCommand"
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
        if logic.is_developer(ctx.author.id):
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
        if logic.is_developer(ctx.author.id):
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

    # Shut down the bot, this cannot be undone from within Discord
    @commands.command()
    async def shutdown(self, ctx: "Context"):
        if logic.is_developer(ctx.author.id):
            await ctx.reply("Cog is shutting down")
            await self.bot.close()
            logic.logging("info", "bot", "Bot closed", {
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "DeveloperCommand"
                }
            })

    # Send an embed explaining the DeveloperCommands
    @commands.command()
    async def help(self, ctx: "Context"):
        if logic.is_developer(ctx.author.id):
            embed = discord.Embed(color=logic.data["bot"]["embed_color"],
                                  title="Developer Help",
                                  description="Explains every DeveloperCommand",
                                  timestamp=dt.now(datetime.UTC))
            embed.set_footer(text="Bot")
            embed.add_field(name="reload_cog <Cog>", value="Reloads a provided Cog. Existing Cogs are:\n- Bot", inline=True)
            embed.add_field(name="unload_cog <Cog>", value="Unloads a before loaded Cog (the same as `reload_cog` can access).\n**WARNING:** once Bot is unloaded it can not be loaded again, use `reload_cog` instead.")
            embed.add_field(name="load_cog <Cog>", value="Loads a before unloaded Cog (the same as `reload_cog` can access).")
            embed.add_field(name="sync", value="Syncs every application command with discord. Needs to be done whenever a command is changed in the source code.", inline=True)
            embed.add_field(name="shutdown", value="shuts down the bot causing it to stop running. This should only be the last escalation step since it is not possible to restart it from within Discord.", inline=True)
            embed.add_field(name="help", value="shows this message.")

            await ctx.reply(embed=embed)
            logic.logging("info", "bot", "DeveloperHelpEmbed sent", {
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "DeveloperCommand"
                }
            })
        else:
            await ctx.reply("This bot supports application (/) commands, please use `/help`")

    # TODO /help command


async def setup(bot) -> None:
    await bot.add_cog(Bot(bot))
