import discord
from discord import app_commands
from discord.ext import commands

from typing import TYPE_CHECKING

import logic

if TYPE_CHECKING:
    from discord.ext.commands import Context


class TwitchCommands(commands.Cog):  # TODO make the messages embeds?
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="add_twitch_commands_role", description="add a role that is allowed to execute the commands known from twitch")
    @app_commands.describe(
        role="the role that you allow to execute the commands"
    )
    @app_commands.default_permissions(manage_guild=True)
    async def add_twitch_commands_role(self, interaction: discord.Interaction, role: discord.Role) -> None:
        if role.id in logic.data["execute_twitch_commands"]:
            role_id = None
            await interaction.response.send_message("Role can already execute Twitch commands")
        else:
            logic.data["execute_twitch_commands"].append(role.id)
            role_id = role.id
            logic.save_data(logic.data, "data.json")
            await interaction.response.send_message("Role added to list")
        logic.logging("info", "twchcmds", "twitch command execution role added", {
            "guild": interaction.guild.id,
            "channel": interaction.channel.id,
            "user": interaction.user.id,
            "added_role": role_id
        })

    @app_commands.command(name="remove_twitch_commands_role", description="forbid a role to execute the commands known from twitch")
    @app_commands.describe(
        role="the role you remove from the list of roles that can execute the commands"
    )
    @app_commands.default_permissions(manage_guild=True)
    async def remove_twitch_commands_role(self, interaction: discord.Interaction, role: discord.Role) -> None:
        if role.id in logic.data["execute_twitch_commands"]:
            logic.data["execute_twitch_commands"].remove(role.id)
            role_id = role.id
            logic.save_data(logic.data, "data.json")
            await interaction.response.send_message("Role removed from list")
        else:
            role_id = None
            await interaction.response.send_message("Role was not able to execute commands before anyway")
        logic.logging("info", "twchcmds", "twitch command execution role removed", {
            "guild": interaction.guild.id,
            "channel": interaction.channel.id,
            "user": interaction.user.id,
            "removed_role": role_id
        })

    @app_commands.command(name="list_twitch_command_roles", description="lists every role that can execute commands know from twitch")
    @app_commands.default_permissions(manage_guild=True)
    async def list_twitch_command_roles(self, interaction: discord.Interaction) -> None:
        if not logic.data["execute_twitch_commands"]:
            await interaction.response.send_message("No role added yet")
        else:
            message_value = ""
            for i in logic.data["execute_twitch_commands"]:
                message_value = message_value + f"<@&{i}>\n"
            embed = discord.Embed.from_dict(logic.embeds["twitch_commands"]["list_entitled_roles"])
            embed.clear_fields()
            embed.add_field(name="Roles", value=message_value)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        logic.logging("info", "twchcmds", "Twitch command roles listed", {
            "guild": interaction.guild.id,
            "channel": interaction.channel.id,
            "user": interaction.user.id
        })


    @commands.command()
    async def ao3(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("check out sina's ao3 [here](https://archiveofourown.org/users/sinaheh/profile):")
            logic.logging("info", "twchcmds", "ao3 social link sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    @commands.command()
    async def patreon(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("BECOME A PATREON MEMBER (to gain early access to the [WEBTOON](https://www.webtoons.com/en/canvas/way-of-the-living-weapon/list?title_no=993451), step-by-step art tutorials, WIPs & lot more extra content) ([patreon link](https://patreon.com/sinaheh))")
            logic.logging("info", "twchcmds", "Patreon social link sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    @commands.command()
    async def pinterest(self, ctx: discord.ext.commands.Context) -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("follow sina on [pinterest](https://www.pinterest.com/sinaheh/)!")
            logic.logging("info", "twchcmds", "Pinterest social link sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    @commands.command()
    async def prints(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("[PRINT SHOP](https://www.inprnt.com/gallery/sinaheh/) IS NOW OPEN")
            logic.logging("info", "twchcmds", "prints social link sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    @commands.command()
    async def socials(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("FOLLOW SINA'S SOCIALS! [twitter](https://www.twitter.com/sinaheh), [main insta](https://www.instagram.com/sinahehlive/), [art insta](https://www.instagram.com/sinahehart/), [tiktok](https://www.tiktok.com/@sinaheh), [tumblr](https://www.tumblr.com/sinaheh), [bluesky](https://bsky.app/profile/sinaheh.bsky.social), [youtube](https://www.youtube.com/@sinaheh)")
            logic.logging("info", "twchcmds", "all social links sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    @commands.command()
    async def spotify(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("[here](https://open.spotify.com/user/sinaxdd/playlists)'s all sina's playlists")
            logic.logging("info", "twchcmds", "Spotify social link sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    @commands.command()
    async def tiktok(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("follow sina on [tiktok](https://www.tiktok.com/@sinaheh)!")
            logic.logging("info", "twchcmds", "TikTok social link sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    @commands.command()
    async def twitter(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("follow sina on twitter! [main](https://twitter.com/sinaheh), [alt](https://twitter.com/sinaltheh)")
            logic.logging("info", "twchcmds", "Twitter social link sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    @commands.command()
    async def wishlist(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("consider buying sina a [gift](https://thronegifts.com/u/sinaheh):")
            logic.logging("info", "twchcmds", "wishlist social link sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    @commands.command()
    async def art(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("sina uses Clip Studio Paint program and HUION Kamvas 22 Plus to draw! ☆ current GO TO brushes can be found [here](https://sinahehbrushes.carrd.co)")
            logic.logging("info", "twchcmds", "art faq sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    # TODO birthday

    @commands.command()
    async def brush(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("find all sina's GO TO brushes [here](https://sinahehbrushes.carrd.co)")
            logic.logging("info", "twchcmds", "brush faq sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    @commands.command()
    async def comms(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("SINA'S [COMMISSIONS](https://drive.google.com/file/d/1x0Wh0QQyXxagA0EZ3NRDwVZSuCyS9r9j/view) ARE OPEN!! if interested you can contact her through instagram DMs or email")
            logic.logging("info", "twchcmds", "commission faq sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    @commands.command()
    async def ocs(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("you can read all about sina's original characters and their lore [here](https://sinahehocs.carrd.co)")
            logic.logging("info", "twchcmds", "original character faq sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    @commands.command()
    async def ocmusic(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("[LEO'S PLAYLIST](https://open.spotify.com/playlist/0KqlAQ1niYOZCByeyoGnP3?si=0149eb8b07024d8f) // [LORIÉN'S PLAYLIST](https://open.spotify.com/playlist/63voqKGasjy8cTAHYBlB4V?si=7fc4f096a3b84924) // [KALEO PLAYLIST](https://open.spotify.com/playlist/5xPg2jGce4P49oM13r21Pz?si=0ee05ae61ca44c4e)")
            logic.logging("info", "twchcmds", "character playlist faq sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    @commands.command()
    async def pronouns(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("sina goes by **she/they**! thank you for asking!!")
            logic.logging("info", "twchcmds", "pronouns faq sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })

    # TODO time/timezone

    @commands.command()
    async def webtoon(self, ctx: "Context") -> None:
        if logic.has_property(logic.data["execute_twitch_commands"], ctx.author.roles):
            await ctx.reply("WAY OF THE LIVING WEAPON IS NOW AVAILABLE ON [WEBTOON](https://www.webtoons.com/en/canvas/way-of-the-living-weapon/list?title_no=993451) AND [TAPAS](https://tapas.io/series/Way-of-the-Living-Weapon/info) ☆ you can get early access to new chapters through my [patreon](https://patreon.com/sinaheh)!")
            logic.logging("info", "twchcmds", "webtoon faq sent", {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id
            })


async def setup(bot) -> None:
    await bot.add_cog(TwitchCommands(bot))
