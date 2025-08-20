import sqlite3
from typing import Optional, TYPE_CHECKING

from lib.getter.config import log_path
from lib.logging.base import command

if TYPE_CHECKING:
    from discord import Interaction


__all__ = [
    "assigning_role"
]


def assigning_role(description: str, interaction: "Interaction", role_id: int, receiver_id: int, reason: Optional[str]) -> int:
    log_id = command("mod", description, interaction, "manager")

    con = sqlite3.connect(log_path())
    con.execute("""
    INSERT INTO assigning_role (role_id, role_id, receiver_id, reason)
    Values (?, ?, ?, ?)
    """, (log_id, role_id, receiver_id, reason))
    con.commit()
    con.close()

    return log_id