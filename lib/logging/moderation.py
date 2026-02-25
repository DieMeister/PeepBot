import sqlite3
from typing import Optional, TYPE_CHECKING

from lib.getter.config import log_path
from lib.logging import command, Module, CommandType

if TYPE_CHECKING:
    from discord import Interaction


__all__ = [
    "assigning_role"
]


def assigning_role(description: str, interaction: "Interaction", role_id: int, receiver_id: int, reason: Optional[str]) -> int:
    """Log adding and removing AssignableRoles as well as the failure of said things.

    Return the log_id.

    Parameters
    -----------
    description: :class:`str`
        A short description of what happened.
    interaction: :class:`Interaction`
        The interaction of the command.
    role_id: :class:`int`
        The discord id of the AssignableRole.
    receiver_id: :class:`int`
        The discord id of the member the AssignableRole is being assigned to.
    reason: Optional[:class:`str`]
        The reason why the member gets or loses the role.
    """
    log_id = command(Module.MODERATION, description, interaction, CommandType.MANAGER)

    con = sqlite3.connect(log_path())
    con.execute("""
    INSERT INTO assigning_role (role_id, role_id, receiver_id, reason)
    Values (?, ?, ?, ?)
    """, (log_id, role_id, receiver_id, reason))
    con.commit()
    con.close()

    return log_id