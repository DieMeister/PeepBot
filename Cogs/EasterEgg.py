from discord.ext import commands
from typing import TYPE_CHECKING

from lib import logging

if TYPE_CHECKING:
    from discord.ext.commands.context import Context


class EasterEgg(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        logging.extension_success("eastregg", "Cog initialised", "setup", "EasterEgg")

    @commands.command()
    async def thx(self, ctx: "Context") -> None:
        await ctx.reply("Thank you Jas and Mono for suffering with me for the whole time")
        logging.command("eastregg", "ThanksMessage sent", ctx, "member")

    @commands.command()
    async def nala(self, ctx: "Context") -> None:
        await ctx.reply("You can't catch Nala, go catch a peep before she bites your toe")
        logging.command("eastregg", "Nala found", ctx, "member")


async def setup(bot) -> None:
    await bot.add_cog(EasterEgg(bot))
