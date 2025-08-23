import sqlite3

from lib.getter.config import database_path

__all__ = [
    "possible_discord_id",
    "assignable_role_in_database"
]


def possible_discord_id(role_id: str) -> bool:
    try:
        int(role_id)
    except ValueError:
        return False
    else:
        return True


def assignable_role_in_database(role_id: int) -> bool:
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