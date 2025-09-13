from discord import app_commands
from discord.app_commands import Group
from discord.ext import commands

from typing import TYPE_CHECKING
from lib import logging, embed, config

if TYPE_CHECKING:
    from discord import Interaction
    from discord.ext.commands.context import Context

class Help(commands.Cog):
    help_commands = Group(name="help", description="provides help")

    def __init__(self, bot):
        self.bot = bot
        logging.extension_success("help", "Cog initialised", "setup", "Help")

    @commands.command()
    async def devhelp(self, ctx: "Context") -> None:
        if ctx.author.id in config.developer():
            await ctx.reply(embed=embed.help.dev())
            logging.help_embed("dev", None, ctx, "developer")
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
                logging.help_embed("config", "peep", interaction, "member")
            case "assignable_roles":
                help_embed = embed.help.config_assignable_role()
                logging.help_embed("config", "assignable_roles", interaction, "member")
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
                logging.help_embed("usage", "peep", interaction, "member")
            case "assignable_roles":
                help_embed = embed.help.use_assignable_roles()
                logging.help_embed("usage", "assignable_roles", interaction, "member")
        await interaction.response.send_message(embed=help_embed)


async def setup(bot) -> None:
    await bot.add_cog(Help(bot))
