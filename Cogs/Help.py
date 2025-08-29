from discord import app_commands
from discord.app_commands import Group
from discord.ext import commands

from typing import TYPE_CHECKING

import lib
from lib import logging, embed
from lib.logging import Module, ExecutionMethod, CommandType, HelpType, HelpCategory

if TYPE_CHECKING:
    from discord import Interaction
    from discord.ext.commands.context import Context

class Help(commands.Cog):
    help_commands = Group(name="help", description="provides help")

    def __init__(self, bot):
        self.bot = bot
        logging.extension_success(Module.HELP, "Cog initialised", ExecutionMethod.SETUP, "Help")

    @commands.command()
    async def devhelp(self, ctx: "Context") -> None:
        if ctx.author.id in lib.get.developer():
            await ctx.reply(embed=embed.help.dev())
            logging.help_embed(HelpType.DEVELOPER, HelpCategory.ALL, ctx, CommandType.DEVELOPER)
        else:
            await ctx.reply("This bot supports application (/) commands, please use `/help`")

    @help_commands.command(name="config", description="provides help configuring the bot")
    @app_commands.choices(
        problem=[
            app_commands.Choice(name="Peep", value="peep"),
            app_commands.Choice(name="AssignableRoles", value="assignable_roles")
        ]
    )
    async def config(self, interaction: "Interaction", problem: app_commands.Choice[str]) -> None:
        match problem.value:
            case "peep":
                help_embed = embed.help.config_peep()
                logging.help_embed(HelpType.CONFIG, HelpCategory.PEEP, interaction, CommandType.MEMBER)
            case "assignable_roles":
                help_embed = embed.help.config_assignable_role()
                logging.help_embed(HelpType.CONFIG, HelpCategory.ASSIGNABLE_ROLES, interaction, CommandType.MEMBER)
        await interaction.response.send_message(embed=help_embed)

    @help_commands.command(name="usage", description="provides help on how to use the Bot")
    @app_commands.choices(
        problem=[
            app_commands.Choice(name="Peep", value="peep"),
            app_commands.Choice(name="AssignableRoles", value="assignable_roles")
        ]
    )
    async def usage(self, interaction: "Interaction", problem: app_commands.Choice[str]) -> None:
        match problem.value:
            case "peep":
                help_embed =  embed.help.use_peep()
                logging.help_embed(HelpType.USAGE, HelpCategory.PEEP, interaction, CommandType.MEMBER)
            case "assignable_roles":
                help_embed = embed.help.use_assignable_roles()
                logging.help_embed(HelpType.USAGE, HelpCategory.ASSIGNABLE_ROLES, interaction, CommandType.MEMBER)
        await interaction.response.send_message(embed=help_embed)


async def setup(bot) -> None:
    await bot.add_cog(Help(bot))
