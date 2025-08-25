from discord import app_commands
from discord.ext import commands

from typing import TYPE_CHECKING

import lib
from lib import logging, embed
from lib.logging import Module, ExecutionMethod, CommandType

if TYPE_CHECKING:
    from discord import Interaction
    from discord.ext.commands.context import Context

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.extension_success(Module.HELP, "Cog initialised", ExecutionMethod.SETUP, "Help")

    @commands.command()
    async def devhelp(self, ctx: "Context") -> None:
        if ctx.author.id in lib.get.developer():
            await ctx.reply(embed=embed.devhelp())
            logging.help_embed("dev", ctx, CommandType.DEVELOPER)
        else:
            await ctx.reply("This bot supports application (/) commands, please use `/help`")

    @app_commands.command(name="help", description="provides help for usage and setup of the bot")
    @app_commands.describe(
        problem="The problem you need help with"
    )
    @app_commands.choices(
        problem=[
            app_commands.Choice(name="Configuration", value="config"),
            app_commands.Choice(name="Usage", value="usage")
        ]
    )
    async def help(self, interaction: "Interaction", problem: app_commands.Choice[str]) -> None:
        if problem.value == "config":
            help_embed = embed.help_config()
            logging.help_embed("setup", interaction, CommandType.MEMBER)
        elif problem.value == "usage":
            help_embed = embed.help_usage()
            logging.help_embed("usage", interaction, CommandType.MEMBER)
        else:
            raise ValueError("HelpEmbedType does not match")
        await interaction.response.send_message(embed=help_embed)


async def setup(bot) -> None:
    await bot.add_cog(Help(bot))