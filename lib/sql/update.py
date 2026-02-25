import sqlite3

from lib.getter.config import database_path


__all__ = [
    "remove_peeps"
]
def remove_peeps(new_total_peeps: int, guild_id: int, user_id: int) -> None:
    """
    Remove peeps from a given member.

    Parameters
    -----------
    new_total_peeps: :class:`int`
        The new total peeps of the member.
    guild_id: :class:`int`
        The member's guild_id
    user_id: :class:`int`
        The member's user id
    """
    data_db = sqlite3.connect(database_path())
    data_db.execute("""
    UPDATE members
    Set
        caught_peeps = ?
        WHERE guild_id = ?
        AND user_id = ?
    """, (new_total_peeps, guild_id, user_id))
    data_db.commit()
    data_db.close()
