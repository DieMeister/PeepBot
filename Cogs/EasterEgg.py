from discord.ext import commands

from typing import TYPE_CHECKING

import logic

if TYPE_CHECKING:
    from discord.ext.commands import Context


class EasterEgg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logic.logging("eastregg", "peep", "Cog initialised", {
            "cog_name": "Peep",
            "command": False
        })

    @commands.command()
    async def thx(self, ctx: "Context"):
        await ctx.reply("Thank you Jas and Mono for suffering with me for the whole time")
        logic.logging("eastregg", "peep", "Member executed !thx", {
            "command": {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id,
                "type": "ManagerCommand",
                "parameters": None
            }
        })


async def setup(bot) -> None:
    await bot.add_cog(EasterEgg(bot))
