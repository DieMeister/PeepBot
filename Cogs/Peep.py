import datetime
from datetime import datetime as dt, timedelta

import discord
from discord import app_commands
from discord.ext import commands

import sqlite3
from typing import TYPE_CHECKING
from random import randint, choice

import lib
from lib import logging, get

if TYPE_CHECKING:
    from discord import Interaction
    from discord.ext.commands.context import Context


class Peep(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        logging.extension_success("peep", "Cog initialised", "setup", "Peep")

    @commands.command()
    async def psps(self, ctx: "Context") -> None:
        timestamp = dt.now(datetime.UTC)

        # get the data of the guild and create a new entry if it doesn't exist
        lib.sql.add_guild(ctx.guild)
        guild = lib.sql.get_guild(ctx.guild.id)
        guild_last_try = get.dt_object(guild[4])

        # check if the used channel is valid
        channel = lib.sql.get_channel(ctx.channel.id)
        if not channel:
            logging.psps_denied(ctx, "Outside of allowed Channel")
            return

        # get the data of the member and create a new entry if it doesn't exist
        lib.sql.add_member(ctx.author)
        member = lib.sql.get_member(ctx.guild.id, ctx.author.id)
        member_last_try = get.dt_object(member[2])
        member_peeps = member[3]
        member_tries = member[4]

        # check if someone else tried within a minute
        if guild_last_try + timedelta(minutes=1) > timestamp:
            logging.psps_denied(ctx, "Within 1 minute of another member")
            return

        # check if the member tried again within their cooldown
        if ctx.author.id in lib.get.vip():
            if member_last_try + timedelta(minutes=5) > timestamp:
                logging.psps_denied(ctx, "vip used twice within 5 minutes")
                return
        elif ctx.author.id in lib.get.vup():
            if member_last_try + timedelta(minutes=30) > timestamp:
                logging.psps_denied(ctx, "vup used twice within 30 minutes")
                return
        elif member_last_try + timedelta(minutes=10) > timestamp:
            logging.psps_denied(ctx, "member used twice within 10 minutes")
            return

        member_tries += 1
        peep_number = randint(1, 7)
        if peep_number == 1:
            steal_number = randint(1, 100)
            # steal peep
            if steal_number == 1:
                thieves = lib.get.thieves()
                mod, emote = choice(list(thieves.items()))
                await ctx.reply(f"{emote} your peep got stolen")
                logging.steal_peep(ctx, mod, emote)
            # give member a peep
            else:
                member_peeps += 1
                await ctx.reply(f"{guild[1]} You have {member_peeps} peeps now")
                logging.catch_peep("Member got a Peep", ctx, member_peeps, peep_number)
        # scratch member
        elif peep_number == 2 or peep_number == 3:
            await ctx.reply(guild[2])
            logging.catch_peep("Member got scratched", ctx, member_peeps, peep_number)
        # don't get a peep
        else:
            await ctx.reply(guild[3])
            logging.catch_peep("Member did not get a Peep", ctx, member_peeps, peep_number)

        # update database
        con = sqlite3.connect(lib.get.database_path())
        con.execute("""
        UPDATE guilds
        SET last_peep = ?
        WHERE guild_id = ?
        """, (get.dt_string(timestamp), ctx.guild.id))
        con.execute("""
        UPDATE members
        SET
            last_peep = ?,
            caught_peeps = ?,
            tries = ?
        WHERE guild_id = ? AND user_id = ?
        """, (get.dt_string(timestamp), member_peeps, member_tries, ctx.guild.id, ctx.author.id))
        con.commit()
        con.close()

    @app_commands.command(name="leaderboard", description="shows the 10 Members with the most Peeps")
    async def leaderboard(self, interaction: "Interaction") -> None:
        connection = sqlite3.connect(lib.get.database_path())
        top_10 = connection.execute("""
           SELECT
               user_id,
               caught_peeps,
               tries
           FROM
               members
           WHERE
               guild_id = ?
           AND
               caught_peeps > 0
           ORDER BY
               caught_peeps DESC,
               user_id ASC
           LIMIT 10
           """, (interaction.guild_id,)).fetchall()

        if not top_10:
            await interaction.response.send_message("nobody got a peep yet")
            logging.command("peep", "Leaderboard sent", interaction, "member")
        else:

            guild = self.bot.get_guild(interaction.guild_id)
            embed = discord.Embed(
                color=lib.get.embed_color(),
                timestamp=dt.now(datetime.UTC)
            )
            for i in top_10:
                member = guild.get_member(i[0])
                if member.nick:
                   name = member.nick
                else:
                    name = member.name
                embed.add_field(
                    name=name,
                    value=f"Peeps: {i[1]}\nTries: {i[2]}",
                    inline=False
                )
            await interaction.response.send_message(embed=embed)
            logging.command("bot", "Leaderboard sent", interaction, "member")

    @app_commands.command(name="rank", description="shows your peeps and total tries")
    async def rank(self, interaction: "Interaction") -> None:
        connection = sqlite3.connect(lib.get.database_path())
        peeps, tries = connection.execute("""
           SELECT
               caught_peeps,
               tries
           FROM
               members
           WHERE
               guild_id = ?
           AND
               user_id = ?
           """, (interaction.guild_id, interaction.user.id)).fetchone()
        await interaction.response.send_message(f"in {tries} tries you got {peeps} peeps")
        logging.command("peep", "RankCommand sent", interaction, "member")


async def setup(bot) -> None:
    await bot.add_cog(Peep(bot))
