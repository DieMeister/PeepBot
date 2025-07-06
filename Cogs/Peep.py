from discord.ext import commands

import datetime
from datetime import datetime as dt, timedelta

from typing import TYPE_CHECKING
from random import randint

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
        guild = logic.get_item(logic.data["guilds"], "guild_id", ctx.guild.id)
        member = logic.get_item(guild["members"], "user_id", ctx.author.id)

        if ctx.channel.id not in guild["allowed_channel_ids"]:
            logic.logging("info", "peep", "Used !psps outside command channel", {
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "UserCommand",
                    "parameters": None
                }
            })
            return

        last_member_count = logic.get_datetime_object(member["execute_psps_timestamp"])
        last_guild_count = logic.get_datetime_object(guild["last_peep"])

        timestamp = dt.now(datetime.UTC)

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
        if ctx.author.id in [729671721975545978, 476491500461621261, 929746020865282059]:
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
        elif ctx.author.id in [662733222903414826, 1084257450846343209]:
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


        member["execute_psps_timestamp"] = logic.get_datetime_string(timestamp)
        guild["last_peep"] = logic.get_datetime_string(timestamp)

        number = randint(1, 7)
        if number == 1:
            member["peep_count"] += 1
            await ctx.reply(f"{guild['peep_success_massage']} You have {member['peep_count']} peeps now")
            logic.logging("info", "peep", "Member got a peep", {
                "peep_count": member["peep_count"],
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
            await ctx.reply(guild["peep_scratch_massage"])
            logic.logging("info", "peep", "Member got scratched", {
                "peep_count": member["peep_count"],
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
            await ctx.reply(guild["peep_no_peep_message"])
            logic.logging("info", "peep", "Member got no peep", {
                "peep_count": member["peep_count"],
                "randint": number,
                "command": {
                    "guild": ctx.guild.id,
                    "channel": ctx.channel.id,
                    "user": ctx.author.id,
                    "type": "UserCommand",
                    "parameters": None
                }
            })
        logic.save_data(logic.data, logic.database_path)


async def setup(bot) -> None:
    await bot.add_cog(Peep(bot))
