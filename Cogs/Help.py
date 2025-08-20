import discord
from discord import app_commands
from discord.ext import commands

import datetime as dt
from datetime import datetime

from typing import TYPE_CHECKING

import lib
from lib import logging

if TYPE_CHECKING:
    from discord import Interaction
    from discord.ext.commands.context import Context

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.extension_success("help", "Cog initialised", "setup", "Help")

    @commands.command()
    async def devhelp(self, ctx: "Context") -> None:
        if ctx.author.id in lib.get.developer():
            embed = discord.Embed(color=lib.get.embed_color(),
                                  title="Developer Help",
                                  description="Explains every DeveloperCommand",
                                  timestamp=datetime(2025, 6, 16, 11, 7, tzinfo=dt.UTC))
            embed.set_footer(text="Bot")
            embed.add_field(name="reload_cog <Cog>",
                            value="Reloads a provided Cog. Existing Cogs are:\n- Bot\n- Peep\n- Config\n- EasterEgg",
                            inline=True)
            embed.add_field(name="unload_cog <Cog>",
                            value="Unloads a before loaded Cog (the same as `reload_cog` can access).\n**WARNING:** once Bot is unloaded it can not be loaded again, use `reload_cog` instead.")
            embed.add_field(name="load_cog <Cog>",
                            value="Loads a before unloaded Cog (the same as `reload_cog` can access).")
            embed.add_field(name="sync",
                            value="Syncs every application command with discord. Needs to be done whenever a command is changed in the source code.",
                            inline=True)
            embed.add_field(name="shutdown",
                            value="shuts down the bot causing it to stop running. This should only be the last escalation step since it is not possible to restart it from within Discord.",
                            inline=True)
            embed.add_field(name="help", value="shows this message.")
            embed.add_field(name="More Help",
                            value="If this didn't explain the question feel free to dm `@diemeister`", inline=False)

            await ctx.reply(embed=embed)
            logging.help_embed("dev", ctx, "developer")
        else:
            await ctx.reply("This bot supports application (/) commands, please use `/help`")

    # FIXME update command
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
            embed.add_field(name="/add_channel <channel>",
                            value="adds a channel as allowed channel. The !psps command works only in allowed channels, everywhere else it will not send a response.")
            embed.add_field(name="/remove_channel <channel>",
                            value="removes a channel as allowed channel. This leads to !psps commands not getting a response anymore.")
            embed.add_field(name="/change_peep_message <message_type> <message>",
                            value="changes the response the bot gives when executing !psps. `message_type` determines which message will be changed, and `message`is the actual response the bot sends.\nNote that the bot automatically adds 'You have {number of peeps} peeps now' after the `You got a peep` message. This can not be turned off.")
            embed.set_footer(text="Bot")

            logging.help_embed("setup", interaction, "member")
        elif problem.value == "usage":
            embed = discord.Embed(
                color=lib.get.embed_color(),
                title="Usage Help",
                timestamp=datetime(2025, 6, 22, 21, 20, tzinfo=dt.UTC)
            )
            embed.add_field(
                name="psps",
                value="- To get peeps type `!psps` in an allowed chat, if you don't know which chats are allowed ask your server manager, admin, or owner. If you are the person responsible to set up the bot please execute /help <setup>\n- You have to wait 10 minutes before you can execute the command again.\n- You have to wait 1 minute after someone else executed the command before you can execute it.",
                inline=False
            )
            embed.add_field(
                name="/rank",
                value="shows the current amount of peeps you have and how often you tried",
                inline=True
            )
            embed.add_field(
                name="/leaderboard",
                value="shows the 10 members of the server with the most peeps",
                inline=True
            )
            embed.set_footer(text="Bot")

            logging.help_embed("usage", interaction, "member")
        else:
            raise ValueError("HelpEmbedType does not match")

        await interaction.response.send_message(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Help(bot))