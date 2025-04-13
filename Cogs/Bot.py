from discord.ext import commands


class Bot(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def sync(self, ctx) -> None:
        await self.bot.tree.sync()
        await ctx.send("Commands synced")


async def setup(bot) -> None:
    await bot.add_cog(Bot(bot))