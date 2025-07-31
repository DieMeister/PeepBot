import datetime
from datetime import datetime as dt, timedelta

from typing import TYPE_CHECKING
from random import randint

from discord.ext import commands
import sqlite3

from lib.date_time import get_datetime_object, get_datetime_string
from lib import logging

import logic

if TYPE_CHECKING:
    from discord.ext.commands import Context


class Peep(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.extension_success("peep", "Cog initialised", "setup")

    @commands.command()
    async def psps(self, ctx: "Context"):
        connection = sqlite3.connect(logic.config["file_paths"]["database"])

        allowed_channel = connection.execute("""
        SELECT *
        FROM allowed_channels
        WHERE channel_id = ?
        """, (ctx.channel.id,)).fetchone()
        if not allowed_channel:
            logging.psps_denied(ctx, "Outside of allowed Channel")
            return

        member = connection.execute("""
        SELECT last_peep, caught_peeps
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
        if ctx.author.id in logic.config["people"]["vip"]:
            if last_member_count + timedelta(minutes=5) > timestamp:
                logging.psps_denied(ctx, "vip used twice within 5 minutes")
                return
        elif ctx.author.id in logic.config["people"]["vup"]:
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
        connection.commit()
        connection.close()


async def setup(bot) -> None:
    await bot.add_cog(Peep(bot))
