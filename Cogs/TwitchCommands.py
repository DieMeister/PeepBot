from discord.ext import commands

import logic


class TwitchCommands(commands.Cog):  # TODO make the messages embeds?
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
        logic.logging("info", "twchcmds", "Patreon social link sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })

    @commands.command()
    async def pinterest(self, ctx) -> None:  # TODO check who is allowed to use this command
        await ctx.reply("follow sina on [pinterest](https://www.pinterest.com/sinaheh/)!")
        logic.logging("info", "twchcmds", "Pinterest social link sent", {
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

    @commands.command()
    async def socials(self, ctx) -> None:  # TODO check who is allowed to use this command
        await ctx.reply("FOLLOW SINA'S SOCIALS! [twitter](https://www.twitter.com/sinaheh), [main insta](https://www.instagram.com/sinahehlive/), [art insta](https://www.instagram.com/sinahehart/), [tiktok](https://www.tiktok.com/@sinaheh), [tumblr](https://www.tumblr.com/sinaheh), [bluesky](https://bsky.app/profile/sinaheh.bsky.social), [youtube](https://www.youtube.com/@sinaheh)")
        logic.logging("info", "twchcmds", "all social links sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })

    @commands.command()
    async def spotify(self, ctx) -> None:  # TODO check who is allowed to use this command
        await ctx.reply("[here](https://open.spotify.com/user/sinaxdd/playlists)'s all sina's playlists")
        logic.logging("info", "twchcmds", "Spotify social link sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })

    @commands.command()
    async def tiktok(self, ctx) -> None:  # TODO check who is allowed to use this command
        await ctx.reply("follow sina on [tiktok](https://www.tiktok.com/@sinaheh)!")
        logic.logging("info", "twchcmds", "TikTok social link sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })


async def setup(bot) -> None:
    await bot.add_cog(TwitchCommands(bot))
