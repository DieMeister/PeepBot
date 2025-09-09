import sqlite3
from lib.getter.config import database_path


__all__ = [
    "assignable_role_in_database"
]


def assignable_role_in_database(role_id: int) -> bool:
    """Return whether a role is an assignable role.

    Parameters
    -----------
    role_id: :class:`int`
        The id of the role that is being checked.
    """
    data_db = sqlite3.connect(database_path())
    role = data_db.execute("""
    SELECT *
    FROM role_assigning
    WHERE role_id = ?
    """, (role_id,)).fetchone()
    data_db.close()
    if role is None:
        return False
    return True