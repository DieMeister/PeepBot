from discord.ext import commands
from discord import app_commands

from typing import TYPE_CHECKING

import logic

if TYPE_CHECKING:
    from discord import Interaction, TextChannel


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logic.logging("info", "peep", "Cog initialised", {
            "cog_name": "Config",
            "command": False
        })

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
    async def change_peep_message(self, interaction: "Interaction", message_type: app_commands.Choice[str],
                                  message: str):
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
    async def add_channel(self, interaction: "Interaction", channel: "TextChannel"):
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
    async def remove_channel(self, interaction: "Interaction", channel: "TextChannel"):
        guild = logic.get_item(logic.data["guilds"], "guild_id", interaction.guild.id)
        if channel.id not in guild["allowed_channel_ids"]:
            await interaction.response.send_message("Channel already not in list")
        else:
            guild["allowed_channel_ids"].remove(channel.id)
            logic.save_data(logic.data, logic.database_path)
            await interaction.response.send_message(f"Channel <#{channel.id}> removed as allowed command channel")
            logic.logging("info", "cnfg", "Channel removed from allowed channel list", {
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


async def setup(bot) -> None:
    await bot.add_cog(Config(bot))
