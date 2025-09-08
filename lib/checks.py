import sqlite3
from typing import Union

from lib.getter.config import database_path

__all__ = [
    "possible_discord_id",
    "assignable_role_in_database"
]


def possible_discord_id(discord_id: Union[str, int]) -> bool:
    """Return whether something could be a discord id.

    Parameters
    -----------
    discord_id: :class:`str`
        the role id that is being checked
    """
    try:
        discord_id = int(discord_id)
    except ValueError:
        pass
    else:
        if discord_id > 10000000000000000:  # 10^16
            return True
    return False


# TODO move to lib.sql
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
