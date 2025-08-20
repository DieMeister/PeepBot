from discord import app_commands, Role, TextChannel, Member
from discord.app_commands import Choice
from discord.ext.commands import Cog

import datetime as dt
from datetime import datetime

from typing import TYPE_CHECKING, Optional
import sqlite3

import lib
from lib import logging
from lib import embed

if TYPE_CHECKING:
    from discord import Interaction


class Moderation(Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.extension_success("mod", "Cog initialised", "setup", "Moderation")

    @staticmethod
    async def possible_role_id(role_id: str) -> bool:
        try:
            int(role_id)
        except ValueError:
            return False
        else:
            return True

    @staticmethod
    async def role_in_database(role_id: int) -> bool:
        con = sqlite3.connect(lib.get.database_path())
        role = con.execute("""
               SELECT *
               FROM role_assigning
               WHERE role_id = ?
               """, (role_id,)).fetchone()
        con.close()
        if role:
            return True
        else:
            return False

    @app_commands.command(name="add_assignable_role", description="add a role others can add to or remove from a user using /add_role or /remove_role")
    @app_commands.describe(role="the role others can add and remove")
    @app_commands.default_permissions(administrator=True)
    async def add_assignable_role(self, interaction: "Interaction", role: Role, reason: Optional[str]) -> None:
        if await self.role_in_database(role.id):
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
        if not await self.possible_role_id(role_id):
            await interaction.response.send_message("Invalid Input")
            logging.invalid_input("mod", "Non-Integer input given to remove AssignableRole from List", interaction, "command", role_id)
            return

        if await self.role_in_database(int(role_id)):
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

    @app_commands.command(name="add_role", description="Add a role to a member")
    @app_commands.describe(
        role_id="the role you want to add",
        member="the member who gets the role",
        reason="this will show up in the AuditLog"
    )
    @app_commands.default_permissions(manage_roles=True)
    # TODO add time restricted option
    async def add_role(self, interaction: "Interaction", role_id: str, member: Member, reason: Optional[str]) -> None:
        if not await self.possible_role_id(role_id):
            await interaction.response.send_message("Invalid Input")
            logging.invalid_input("mod", "Non-Integer input given to assign Role to Member", interaction, "manager", role_id)
            return
        if not await self.role_in_database(int(role_id)):
            await interaction.response.send_message("This Role is not available to assign to other Members")
            logging.assigning_role("Tried to assign Role to Member that is not possible to select", interaction, int(role_id), member.id, reason)
            return
        role = interaction.guild.get_role(int(role_id))
        if role in member.roles:
            await interaction.response.send_message("Member already has this role")
            logging.assigning_role("Added AssignableRole that Member already has", interaction, role.id, member.id, reason)
            return
        await member.add_roles(role, reason=reason)

        log_id = logging.assigning_role("Role given to Member", interaction, role.id, member.id, reason)
        log_channel = lib.get.log_channel(interaction.guild)
        if log_channel is not None:
            await log_channel.send(embed=embed.role_log(str(log_id), "Role added to Member", str(role_id), str(interaction.user.id), reason, str(member.id)))
            await interaction.response.send_message("Role added to Member")
        else:
            await interaction.response.send_message(f"Role added to Member {lib.get.log_channel_missing()}")


    @app_commands.command(name="remove_role", description="Remove a role from a member")
    @app_commands.describe(
        role_id="the role you want to remove",
        member="the member who gets the role removed",
    )
    @app_commands.default_permissions(manage_roles=True)
    async def remove_role(self, interaction: "Interaction", role_id: str, member: Member, reason: Optional[str]) -> None:
        if not await self.possible_role_id(role_id):
            await interaction.response.send_message("Invalid Input")
            logging.invalid_input("mod", "Non-Integer input given to remove Role from Member", interaction, "manager", role_id)
            return
        if not await self.role_in_database(int(role_id)):
            await interaction.response.send_message("This Role is not available to remove from other Members")
            logging.assigning_role("Tried to remove Role from Member that is not possible to select", interaction, int(role_id), member.id, reason)
            return
        role = interaction.guild.get_role(int(role_id))
        if role not in member.roles:
            await interaction.response.send_message("Member already does not have this role")
            logging.assigning_role("Removed AssignableRole that Member doesn't have", interaction, role.id, member.id, reason)
            return
        await member.remove_roles(role, reason="execution of /remove_role")
        log_id = logging.assigning_role("Role removed from Member", interaction, role.id, member.id, reason)
        log_channel = lib.get.log_channel(interaction.guild)
        if log_channel is not None:
            await log_channel.send(
                embed=embed.role_log(str(log_id), "Role removed from Member", str(role_id), str(interaction.user.id), reason, str(member.id)))
            await interaction.response.send_message("Role removed from Member")
        else:
            await interaction.response.send_message(f"Role removed from Member {lib.get.log_channel_missing()}")

    @remove_assignable_role.autocomplete("role_id")
    @add_role.autocomplete("role_id")
    @remove_role.autocomplete("role_id")
    async def autocomplete(self, interaction: "Interaction", current: str) -> list[Choice[int]]:
        con = sqlite3.connect(lib.get.database_path())
        roles = con.execute("""
        SELECT role_id
        FROM role_assigning
        WHERE guild_id = ?
        """, (interaction.guild_id,)).fetchall()
        choices = []
        for i in roles:
            role = interaction.guild.get_role(i[0])
            if role and ((current in role.name) or (current == str(role.id))):
                choices.append(Choice(name=role.name, value=str(role.id)))
        return choices

    @app_commands.command(name="set_log_channel", description="Set the channel where the bot sends its log messages to")
    @app_commands.describe(channel="the channel you set as new LogChanel")
    @app_commands.default_permissions(administrator=True)
    async def set_log_channel(self, interaction: "Interaction", channel: TextChannel) -> None:
        con = sqlite3.connect(lib.get.database_path())
        guild = con.execute("""
        SELECT *
        FROM guilds
        WHERE guild_id = ?
        """, (interaction.guild_id,)).fetchone()
        if guild is None:
            lib.sql.add_guild(interaction.guild, datetime.now(dt.UTC))
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
    await bot.add_cog(Moderation(bot))

