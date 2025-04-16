from discord.ext import commands

import logic


class TwitchCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def ao3(self, ctx) -> None:  # TODO check who is allowed to use the command
        await ctx.reply("check out sina's ao3 [here](https://archiveofourown.org/users/sinaheh/profile):")
        logic.logging("info", "twchcmds", "ao3 link sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })


async def setup(bot) -> None:
    await bot.add_cog(TwitchCommands(bot))
