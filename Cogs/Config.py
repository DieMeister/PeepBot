from discord import Role
from discord import app_commands, TextChannel
from discord.ext import commands

from typing import TYPE_CHECKING, Optional
import sqlite3

import lib
from lib import logging, embed, assignable_role_in_database, possible_discord_id
from lib.logging import Module, ExecutionMethod, CommandType

if TYPE_CHECKING:
    from discord import Interaction


class Config(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        logging.extension_success(Module.CONFIG, "Cog initialised", ExecutionMethod.SETUP, "Config")

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
    async def change_peep_message(self, interaction: "Interaction", message_type: app_commands.Choice[str], message: str) -> None:
        lib.sql.add_guild(interaction.guild)

        con = sqlite3.connect(lib.get.database_path())
        old_message = con.execute("""
        SELECT ?
        FROM guilds
        WHERE guild_id = ?
        """, (message_type.value, interaction.guild_id)).fetchone()[0]

        con.execute(f"""
        UPDATE guilds
        SET {message_type.value} = ?
        WHERE guild_id = ?
        """, (message, interaction.guild_id))
        con.commit()

        await interaction.response.send_message(f"New Message set to '{message}'")
        logging.change_peep_message(interaction, message_type.value, old_message, message)
        con.close()

    @app_commands.command(name="add_psps_channel", description="adds a channel where commands can be used")
    @app_commands.describe(channel="The channel that is added to the allowed list")
    @app_commands.default_permissions(manage_guild=True)
    async def add_psps_channel(self, interaction: "Interaction", channel: TextChannel) -> None:
        lib.sql.add_guild(interaction.guild)
        connection = sqlite3.connect(lib.get.database_path())

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
            logging.configure_channel(Module.CONFIG, "Channel added", interaction, channel)
        connection.close()


    @app_commands.command(name="remove_psps_channel", description="removes a channel where commands can be used")
    @app_commands.describe(channel="The channel that is being removed form the list of allowed channels")
    @app_commands.default_permissions(manage_guild=True)
    async def remove_psps_channel(self, interaction: "Interaction", channel: TextChannel) -> None:
        lib.sql.add_guild(interaction.guild)
        connection = sqlite3.connect(lib.get.database_path())

        if not connection.execute(f"SELECT * FROM allowed_channels WHERE channel_id = {channel.id}"):
            await interaction.response.send_message("Channel already not in list")
        else:
            connection.execute(f"""
            DELETE FROM allowed_channels
            WHERE channel_id = {channel.id}
            """)
            connection.commit()

            await interaction.response.send_message(f"Channel <#{channel.id}> removed as allowed command channel")
            logging.configure_channel(Module.CONFIG, "Channel removed", interaction, channel)
        connection.close()

    @app_commands.command(name="add_assignable_role", description="add a role others can add to or remove from a user using /add_role or /remove_role")
    @app_commands.describe(role="the role others can add and remove")
    @app_commands.default_permissions(administrator=True)
    async def add_assignable_role(self, interaction: "Interaction", role: Role, reason: Optional[str]) -> None:
        if assignable_role_in_database(role.id):
            await interaction.response.send_message("This role is already added")
            logging.change_of_assignable_roles("Tried to add already existing AssignableRole to List", interaction, role.id, reason)
        else:
            con = sqlite3.connect(lib.get.database_path())
            con.execute("""
            INSERT INTO role_assigning (role_id, guild_id)
            VALUES (?, ?)
            """, (role.id, interaction.guild_id))
            con.commit()

            log_channel = lib.get.log_channel(interaction.guild)
            log_id =  logging.change_of_assignable_roles("AssignableRole added to List", interaction, role.id, reason)
            if log_channel is None:
                await interaction.response.send_message(f"Role added {lib.get.log_channel_missing()}")
            else:
                await interaction.response.send_message("Role added")
                await log_channel.send(embed=embed.role_log(str(log_id), "AssignableRole added to List", str(role.id), str(interaction.user.id), reason))

    @app_commands.command(
        name="remove_assignable_role",
        description="remove a role others can add to or remove from a user using /add_role or /remove_role"
    )
    @app_commands.describe(role_id="the role others can no longer add or remove")
    @app_commands.default_permissions(administrator=True)
    async def remove_assignable_role(self, interaction: "Interaction", role_id: str, reason: Optional[str]) -> None:
        if not possible_discord_id(role_id):
            await interaction.response.send_message("Invalid Input")
            logging.invalid_input(Module.MODERATION, "Non-Integer input given to remove AssignableRole from List", interaction, CommandType.ADMIN, role_id)
            return

        if assignable_role_in_database(int(role_id)):
            con = sqlite3.connect(lib.get.database_path())
            con.execute("""
            DELETE FROM role_assigning
            WHERE role_id = ?
            """, (int(role_id),))
            con.commit()
            con.close()

            log_id = logging.change_of_assignable_roles("AssignableRole removed from List", interaction, int(role_id), reason)
            log_channel = lib.get.log_channel(interaction.guild)
            if log_channel is None:
                await interaction.response.send_message(f"Role removed {lib.get.log_channel_missing()}")
            else:
                await interaction.response.send_message("Role removed")
                await log_channel.send(embed=embed.role_log(str(log_id), "AssignableRole removed from List", role_id, str(interaction.user.id), reason))
        else:
            await interaction.response.send_message("Role was already not added")
            logging.change_of_assignable_roles("Tried to remove not-added AssignableRole from List", interaction, int(role_id), reason)

    @app_commands.command(name="set_log_channel", description="Set the channel where the bot sends its log messages to")
    @app_commands.describe(channel="the channel you set as new LogChanel")
    @app_commands.default_permissions(administrator=True)
    async def set_log_channel(self, interaction: "Interaction", channel: TextChannel) -> None:
        lib.sql.add_guild(interaction.guild)
        con = sqlite3.connect(lib.get.database_path())
        con.execute("""
        UPDATE guilds
        SET log_channel_id = ?
        WHERE guild_id = ?
        """, (channel.id, interaction.guild_id))
        con.commit()
        con.close()
        await interaction.response.send_message("Channel set")
        log_id = logging.set_log_channel(interaction, channel.id)
        await channel.send(embed=embed.channel_log(str(log_id), "LogChannel set", str(channel.id), str(interaction.user.id)))


async def setup(bot) -> None:
    await bot.add_cog(Config(bot))
