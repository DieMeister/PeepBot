import sqlite3
from discord.app_commands import Choice
from typing import TYPE_CHECKING

from lib.getter import database_path
from Cogs.Moderation import Moderation
from Cogs.Config import Config

if TYPE_CHECKING:
    from discord import Interaction


__all__ = [
    "autocomplete"
]


@Config.remove_assignable_role.autocomplete("role_id")
@Moderation.add_role.autocomplete("role_id")
@Moderation.remove_role.autocomplete("role_id")
async def autocomplete(interaction: "Interaction", current: str) -> list[Choice[int]]:
    """Return every assignable role that contains the given input."""
    con = sqlite3.connect(database_path())
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
