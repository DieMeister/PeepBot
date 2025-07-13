import datetime
from datetime import datetime as dt, timedelta

from typing import TYPE_CHECKING
from random import randint

from discord.ext import commands
import sqlite3

from lib.date_time import get_datetime_object, get_datetime_string
import logic

if TYPE_CHECKING:
    from discord.ext.commands import Context


class Peep(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logic.logging("info", "peep", "Cog initialised", {
            "cog_name": "Peep",
            "command": False
        })

    @commands.command()
    async def psps(self, ctx: "Context"):
        connection = sqlite3.connect(logic.config["file_paths"]["database"])

        allowed_channel = connection.execute("""
        SELECT *
        FROM allowed_channels
        WHERE channel_id = ?
        """, (ctx.channel.id,)).fetchone()
        if not allowed_channel:
            logic.logging("info", "peep", "Used !psps outside allowed channel", {
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "UserCommand",
                    "parameters": None
                }
            })
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
            logic.logging("info", "peep", "Used !psps within 1 minute of another person", {
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "UserCommand",
                    "parameters": None
                }
            })
            return
        if ctx.author.id in logic.config["people"]["vip"]:
            if last_member_count + timedelta(minutes=5) > timestamp:
                logic.logging("info", "peep", "Used !psps within within 5 minutes of last use", {
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "UserCommand",
                        "parameters": None
                    }
                })
                return
        elif ctx.author.id in logic.config["people"]["vup"]:
            if last_member_count + timedelta(minutes=30) > timestamp:
                logic.logging("info", "peep", "Used !psps within within 30 minutes of last use", {
                    "command": {
                        "guild": ctx.guild.id,
                        "channel": ctx.channel.id,
                        "user": ctx.author.id,
                        "type": "UserCommand",
                        "parameters": None
                    }
                })
                return
        elif last_member_count + timedelta(minutes=10) > timestamp:
            logic.logging("info", "peep", "Used !psps within within 10 minutes of last use", {
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "UserCommand",
                    "parameters": None
                }
            })
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
            logic.logging("info", "peep", "Member got a peep", {
                "peep_count": new_count,
                "randint": number,
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "UserCommand",
                    "parameters": None
                }
            })
        elif number == 2 or number == 3:
            await ctx.reply(guild[2])
            logic.logging("info", "peep", "Member got scratched", {
                "peep_count": member[1],
                "randint": number,
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "UserCommand",
                    "parameters": None
                }
            })
        else:
            await ctx.reply(guild[3])
            logic.logging("info", "peep", "Member got no peep", {
                "peep_count": member[1],
                "randint": number,
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "UserCommand",
                    "parameters": None
                }
            })
        connection.commit()
        connection.close()


async def setup(bot) -> None:
    await bot.add_cog(Peep(bot))
