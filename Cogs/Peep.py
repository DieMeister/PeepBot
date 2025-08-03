import datetime
from datetime import datetime as dt, timedelta

import discord
from discord import app_commands
from discord.ext import commands

import sqlite3
from typing import TYPE_CHECKING
from random import randint

import lib
from lib import logging, get_datetime_object, get_datetime_string

if TYPE_CHECKING:
    from discord import Interaction
    from discord.ext.commands.context import Context


class Peep(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        logging.extension_success("peep", "Cog initialised", "setup", "Peep")

    @commands.command()
    async def psps(self, ctx: "Context") -> None:
        connection = sqlite3.connect(lib.get.database_path())

        allowed_channel = connection.execute("""
        SELECT *
        FROM allowed_channels
        WHERE channel_id = ?
        """, (ctx.channel.id,)).fetchone()
        if not allowed_channel:
            logging.psps_denied(ctx, "Outside of allowed Channel")
            return

        member = connection.execute("""
        SELECT last_peep, caught_peeps, tries
        FROM members
        WHERE user_id = ?
        AND guild_id = ?
        """, (ctx.author.id, ctx.guild.id)).fetchone()
        guild = connection.execute("""
        SELECT last_peep, success_message, scratch_message, no_peep_message
        FROM guilds
        WHERE guild_id = ?
        """, (ctx.guild.id,)).fetchone()

        timestamp = dt.now(datetime.UTC)
        last_member_count = get_datetime_object(member[0])
        last_guild_count = get_datetime_object(guild[0])

        if last_guild_count + timedelta(minutes=1) > timestamp:
            logging.psps_denied(ctx, "Within 1 minute of another member")
            return
        if ctx.author.id in lib.get.vip():
            if last_member_count + timedelta(minutes=5) > timestamp:
                logging.psps_denied(ctx, "vip used twice within 5 minutes")
                return
        elif ctx.author.id in lib.get.vup():
            if last_member_count + timedelta(minutes=30) > timestamp:
                logging.psps_denied(ctx, "vup used twice within 30 minutes")
                return
        elif last_member_count + timedelta(minutes=10) > timestamp:
            logging.psps_denied(ctx, "member used twice within 10 minutes")
            return

        connection.execute("""
        UPDATE members
        SET last_peep = ?
        WHERE user_id = ?
        AND guild_id = ?
        """, (get_datetime_string(timestamp), ctx.author.id, ctx.guild.id))
        connection.execute("""
        UPDATE guilds
        SET last_peep = ?
        WHERE guild_id = ?
        """, (get_datetime_string(timestamp), ctx.guild.id))

        number = randint(1, 7)
        if number == 1:
            new_count = member[1] + 1
            connection.execute("""
            UPDATE members
            SET caught_peeps = ?
            WHERE user_id = ?
            AND guild_id = ?
            """, (new_count, ctx.author.id, ctx.guild.id))

            await ctx.reply(f"{guild[1]} You have {new_count} peeps now")
            logging.catch_peep("Member got a Peep", ctx, new_count, number)
        elif number == 2 or number == 3:
            await ctx.reply(guild[2])
            logging.catch_peep("Member got scratched", ctx, member[1], number)
        else:
            await ctx.reply(guild[3])
            logging.catch_peep("Member did not get a Peep", ctx, member[1], number)

        tries = member[2] + 1
        connection.execute("""
        UPDATE members
        SET tries = ?
        WHERE user_id = ?
        AND guild_id = ?
        """, (tries, ctx.author.id, ctx.guild.id))
        connection.commit()
        connection.close()

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
            logging.command("bot", "Leaderboard sent", interaction, "member")
        else:

            guild = self.bot.get_guild(interaction.guild_id)
            embed = discord.Embed(
                color=lib.get.embed_color(),
                timestamp=dt.now(datetime.UTC)
            )
            for i in top_10:
                member = guild.get_member(i[0])
                embed.add_field(
                    name=member.nick,
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
        logging.command("bot", "RankCommand sent", interaction, "member")


async def setup(bot) -> None:
    await bot.add_cog(Peep(bot))
