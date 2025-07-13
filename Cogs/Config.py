from discord.ext import commands
from discord import app_commands
from discord import TextChannel

from typing import TYPE_CHECKING
import sqlite3

import logic

if TYPE_CHECKING:
    from discord import Interaction


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
            app_commands.Choice(name="No Peep", value="no_peep_message"),
            app_commands.Choice(name="Peep scratched you", value="scratch_massage"),
            app_commands.Choice(name="You got a peep", value="success_massage")
        ]
    )
    @app_commands.default_permissions(manage_guild=True)
    async def change_peep_message(self, interaction: "Interaction", message_type: app_commands.Choice[str], message: str):
        connection = sqlite3.connect(logic.config["file_paths"]["database"])

        connection.execute(f"""
        UPDATE guilds
        SET {message_type.value} = ?
        WHERE guild_id = ?
        """, (message, interaction.guild_id))
        connection.commit()

        await interaction.response.send_message(f"New Message set to '{message}'")
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
        connection.close()

    @app_commands.command(name="add_channel", description="adds a channel where commands can be used")
    @app_commands.describe(channel="The channel that is added to the allowed list")
    @app_commands.default_permissions(manage_guild=True)
    async def add_channel(self, interaction: "Interaction", channel: TextChannel):
        connection = sqlite3.connect(logic.config["file_paths"]["database"])

        known_channel = connection.execute("""
        SELECT *
        FROM allowed_channels
        WHERE channel_id = ?
        """, (channel.id,)).fetchone()
        if known_channel:
            await interaction.response.send_message("Channel already in list")
        else:
            connection.execute("""
            INSERT INTO allowed_channels 
            VALUES (?, ?)
            """, (channel.id, interaction.guild_id))
            connection.commit()

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
        connection.close()


    @app_commands.command(name="remove_channel", description="removes a channel where commands can be used")
    @app_commands.describe(channel="The channel that is being removed form the list of allowed channels")
    @app_commands.default_permissions(manage_guild=True)
    async def remove_channel(self, interaction: "Interaction", channel: TextChannel):
        connection = sqlite3.connect(logic.config["file_paths"]["database"])

        if not connection.execute(f"SELECT * FROM allowed_channels WHERE channel_id = {channel.id}"):
            await interaction.response.send_message("Channel already not in list")
        else:
            connection.execute(f"""
            DELETE FROM allowed_channels
            WHERE channel_id = {channel.id}
            """)
            connection.commit()

            await interaction.response.send_message(f"Channel <#{channel.id}> removed as allowed command channel")
            logic.logging("info", "config", "Channel removed from allowed channel list", {
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
        connection.close()


async def setup(bot) -> None:
    await bot.add_cog(Config(bot))
