from discord.ext import commands

import logic


class TwitchCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def ao3(self, ctx) -> None:  # TODO check who is allowed to use this command
        await ctx.reply("check out sina's ao3 [here](https://archiveofourown.org/users/sinaheh/profile):")
        logic.logging("info", "twchcmds", "ao3 social link sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })

    @commands.command()
    async def patreon(self, ctx) -> None:  # TODO check who is allowed to use this command
        await ctx.reply("BECOME A PATREON MEMBER (to gain early access to the [WEBTOON](https://www.webtoons.com/en/canvas/way-of-the-living-weapon/list?title_no=993451), step-by-step art tutorials, WIPs & lot more extra content) ([patreon link](https://patreon.com/sinaheh))")
        logic.logging("info", "twchcmds", "patreon social link sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })

    @commands.command()
    async def pinterest(self, ctx) -> None:  # TODO check who is allowed to use this command
        await ctx.reply("follow sina on [pinterest](https://www.pinterest.com/sinaheh/)!")
        logic.logging("info", "twchcmds", "pinterest social link sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })

    @commands.command()
    async def prints(self, ctx) -> None:  # TODO check who is allowed to use this command
        await ctx.reply("[PRINT SHOP](https://www.inprnt.com/gallery/sinaheh/) IS NOW OPEN")
        logic.logging("info", "twchcmds", "prints social link sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })


async def setup(bot) -> None:
    await bot.add_cog(TwitchCommands(bot))
