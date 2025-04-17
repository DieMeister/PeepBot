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

    @commands.command()
    async def twitter(self, ctx) -> None:  #TODO check who is allowed to use this command
        await ctx.reply("follow sina on twitter! [main](https://twitter.com/sinaheh), [alt](https://twitter.com/sinaltheh)")
        logic.logging("info", "twchcmds", "Twitter social link sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })

    @commands.command()
    async def wishlist(self, ctx) -> None:
        await ctx.reply("consider buying sina a [gift](https://thronegifts.com/u/sinaheh):")
        logic.logging("info", "twchcmds", "wishlist social link sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })

    @commands.command()
    async def art(self, ctx) -> None:
        await ctx.reply("sina uses Clip Studio Paint program and HUION Kamvas 22 Plus to draw! ☆ current GO TO brushes can be found [here](https://sinahehbrushes.carrd.co)")
        logic.logging("info", "twchcmds", "art faq sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })

    # TODO birthday

    @commands.command()
    async def brush(self, ctx) -> None:
        await ctx.reply("find all sina's GO TO brushes [here](https://sinahehbrushes.carrd.co)")
        logic.logging("info", "twchcmds", "brush faq sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })

    @commands.command()
    async def comms(self, ctx) -> None:
        await ctx.reply("SINA'S [COMMISSIONS](https://drive.google.com/file/d/1x0Wh0QQyXxagA0EZ3NRDwVZSuCyS9r9j/view) ARE OPEN!! if interested you can contact her through instagram DMs or email")
        logic.logging("info", "twchcmds", "commission faq sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })

    @commands.command()
    async def ocs(self, ctx) -> None:
        await ctx.reply("you can read all about sina's original characters and their lore [here](https://sinahehocs.carrd.co)")
        logic.logging("info", "twchcmds", "original character faq sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })

    @commands.command()
    async def ocmusic(self, ctx) -> None:
        await ctx.reply("[LEO'S PLAYLIST](https://open.spotify.com/playlist/0KqlAQ1niYOZCByeyoGnP3?si=0149eb8b07024d8f) // [LORIÉN'S PLAYLIST](https://open.spotify.com/playlist/63voqKGasjy8cTAHYBlB4V?si=7fc4f096a3b84924) // [KALEO PLAYLIST](https://open.spotify.com/playlist/5xPg2jGce4P49oM13r21Pz?si=0ee05ae61ca44c4e)")
        logic.logging("info", "twchcmds", "character playlist faq sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })

    @commands.command()
    async def pronouns(self, ctx) -> None:
        await ctx.reply("sina goes by **she/they**! thank you for asking!!")
        logic.logging("info", "twchcmds", "pronouns faq sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })

    @commands.command()
    async def webtoon(self, ctx) -> None:
        await ctx.reply("WAY OF THE LIVING WEAPON IS NOW AVAILABLE ON [WEBTOON](https://www.webtoons.com/en/canvas/way-of-the-living-weapon/list?title_no=993451) AND [TAPAS](https://tapas.io/series/Way-of-the-Living-Weapon/info) ☆ you can get early access to new chapters through my [patreon](https://patreon.com/sinaheh)!")
        logic.logging("info", "twchcmds", "webtoon faq sent", {
            "guild": ctx.guild.id,
            "channel": ctx.channel.id,
            "user": ctx.author.id
        })


async def setup(bot) -> None:
    await bot.add_cog(TwitchCommands(bot))
