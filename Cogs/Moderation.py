from discord import app_commands, Member
from discord.ext.commands import Cog

from typing import TYPE_CHECKING, Optional

import lib
from lib import logging, embed, possible_discord_id
from lib.sql import assignable_role_in_database

if TYPE_CHECKING:
    from discord import Interaction


class Moderation(Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.extension_success("mod", "Cog initialised", "setup", "Moderation")

    @app_commands.command(name="add_role", description="Add a role to a member")
    @app_commands.describe(
        role_id="the role you want to add",
        member="the member who gets the role",
        reason="this will show up in the AuditLog"
    )
    @app_commands.default_permissions(manage_roles=True)
    async def add_role(self, interaction: "Interaction", role_id: str, member: Member, reason: Optional[str]) -> None:
        if not possible_discord_id(role_id):
            await interaction.response.send_message("Invalid Input")
            logging.invalid_input("mod", "Non-Integer input given to assign Role to Member", interaction, "manager", role_id)
            return
        if not assignable_role_in_database(int(role_id)):
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
        if not possible_discord_id(role_id):
            await interaction.response.send_message("Invalid Input")
            logging.invalid_input("mod", "Non-Integer input given to remove Role from Member", interaction, "manager", role_id)
            return
        if not assignable_role_in_database(int(role_id)):
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


async def setup(bot) -> None:
    await bot.add_cog(Moderation(bot))

