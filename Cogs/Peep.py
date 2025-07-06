import discord
from discord.ext import commands
from discord import app_commands

import datetime
from datetime import datetime as dt, timedelta

from typing import TYPE_CHECKING
from random import randint

import logic

if TYPE_CHECKING:
    from discord.ext.commands import Context
    from discord import Interaction


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


    @app_commands.command(name="change_peep_message", description="changes the response a member gets when using !psps")
    @app_commands.describe(
        message_type="Which message you want to change",
        message="The new message that is going to be sent"
    )
    @app_commands.choices(
        message_type=[
            app_commands.Choice(name="No Peep", value="peep_no_peep_message"),
            app_commands.Choice(name="Peep scratched you", value="peep_scratch_massage"),
            app_commands.Choice(name="You got a peep", value="peep_success_massage")
        ]
    )
    @app_commands.default_permissions(manage_guild=True)
    async def change_peep_message(self, interaction: "Interaction", message_type: app_commands.Choice[str], message: str):
        guild = logic.get_item(logic.data["guilds"], "guild_id", interaction.guild.id)
        guild[message_type.value] = message
        await interaction.response.send_message(f"New Message set to '{message}'")
        logic.save_data(logic.data, logic.database_path)
        logic.logging("info", "peep", "PeepMessage changed", {
            "command": {
                "guild": interaction.guild.id,
                "channel": interaction.channel.id,
                "user": interaction.user.id,
                "type": "ManagerCommand",
                "parameters": {
                    "message_type": message_type.value,
                    "message": message
                }
            }
        })

    @app_commands.command(name="add_channel", description="adds a channel where commands can be used")
    @app_commands.describe(channel="The channel that is added to the allowed list")
    @app_commands.default_permissions(manage_guild=True)
    async def add_channel(self, interaction: "Interaction", channel: discord.TextChannel):
        guild = logic.get_item(logic.data["guilds"], "guild_id", interaction.guild.id)
        if channel.id in guild["allowed_channel_ids"]:
            await interaction.response.send_message("Channel already in list")
        else:
            guild["allowed_channel_ids"].append(channel.id)
            logic.save_data(logic.data, logic.database_path)
            await interaction.response.send_message(f"Channel <#{channel.id}> added as allowed command channel")
            logic.logging("info", "peep", "Channel added to allowed channel list", {
                "command": {
                    "guild": interaction.guild.id,
                    "channel": interaction.channel.id,
                    "user": interaction.user.id,
                    "type": "ManagerCommand",
                    "parameters": {
                        "channel": [
                            interaction.channel.id,
                            interaction.channel.name
                        ]
                    }
                }
            })

    @app_commands.command(name="remove_channel", description="removes a channel where commands can be used")
    @app_commands.describe(channel="The channel that is being removed form the list of allowed channels")
    @app_commands.default_permissions(manage_guild=True)
    async def remove_channel(self, interaction: "Interaction", channel: discord.TextChannel):
        guild = logic.get_item(logic.data["guilds"], "guild_id", interaction.guild.id)
        if channel.id not in guild["allowed_channel_ids"]:
            await interaction.response.send_message("Channel already not in list")
        else:
            guild["allowed_channel_ids"].remove(channel.id)
            logic.save_data(logic.data, logic.database_path)
            await interaction.response.send_message(f"Channel <#{channel.id}> removed as allowed command channel")
            logic.logging("info", "peep", "Channel removed from allowed channel list", {
                "command": {
                    "guild": interaction.guild.id,
                    "channel": interaction.channel.id,
                    "user": interaction.user.id,
                    "type": "ManagerCommand",
                    "parameters": {
                        "channel": [
                            interaction.channel.id,
                            interaction.channel.name
                        ]
                    }
                }
            })

    @commands.command()
    async def thx(self, ctx: "Context"):
        await ctx.reply("Thank you Jas and Mono for suffering with me for the whole time")
        logic.logging("info", "peep", "Member executed !thx", {
            "command": {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "user": ctx.author.id,
                "type": "ManagerCommand",
                "parameters": None
            }
        })


async def setup(bot) -> None:
    await bot.add_cog(Peep(bot))
