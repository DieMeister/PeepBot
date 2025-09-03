import sqlite3

from lib.getter.config import database_path

__all__ = [
    "possible_discord_id",
    "assignable_role_in_database"
]


def possible_discord_id(role_id: str) -> bool:
    """Return whether a :class:`str` can be converted into a discord id.

    Parameters
    -----------
    role_id: :class:`str`
        the role id that is being checked
    """
    try:
        int(role_id)
    except ValueError:
        return False
    else:
        return True


def assignable_role_in_database(role_id: int) -> bool:
    """Return whether a role is an assignable ole.

    Parameters
    -----------
    role_id: :class:`int`
        The id of the role that is being checked.
    """
    con = sqlite3.connect(database_path())
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