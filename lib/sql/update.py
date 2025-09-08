import sqlite3
from typing import TYPE_CHECKING

from lib.getter.config import database_path

if TYPE_CHECKING:
    from lib import types


__all__ = [
    "get_peeps",
    "remove_peeps"
]


# TODO maybe calculate the new values here and only get the amount it changes
def get_peeps(new_caught_peeps: int, new_received_peeps: int, guild_id: int, user_id: int) -> "types.sql.Member":
    """
    Update the bot's database when a member gets peeps gifted and return the member's data.

    Parameters
    -----------
    new_caught_peeps: :class:`int`
        The new amount of peeps the member has.
    new_received_peeps: :class:`int`
        The new amount of peeps the member got gifted.
    guild_id: :class:`int`
        The member's guild id
    user_id: :class:`int`
        The member's user id
    """
    data_db = sqlite3.connect(database_path())
    member_data: "types.sql.Member" = data_db.execute("""
    UPDATE TABLE members
    SET
        caught_peeps = ?,
        received_peeps = ?
    WHERE guild_id = ?
    AND user_id = ?
    RETURNING
        user_id,
        guild_id,
        last_peep,
        caught_peeps,
        tries,
        sent_peeps,
        received_peeps
    """, (new_caught_peeps, new_received_peeps, guild_id, user_id)).fetchone()
    data_db.commit()
    data_db.close()
    return member_data


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
