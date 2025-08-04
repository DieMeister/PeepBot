import sqlite3

from .getter import developer, database_path


__all__ = [
    "is_developer",
    "is_guild_in_database",
    "is_member_in_database"
]


def is_developer(user_id: int) -> bool:
    """Check if a member is a developer of the Bot."""
    if user_id in developer():
        return True
    return False


def is_guild_in_database(guild_id: int) -> bool:
    con = sqlite3.connect(database_path())
    guild = con.execute("""
    SELECT *
    FROM guilds
    WHERE guild_id = ?
    """, (guild_id,)).fetchall()
    con.close()

    if guild:
        return True
    return False


def is_member_in_database(guild_id: int, user_id: int) -> bool:
    con = sqlite3.connect(database_path())
    member = con.execute("""
    SELECT *
    FROM members
    WHERE guild_id = ?
    AND user_id = ?
    """, (guild_id, user_id)).fetchall()
    con.close()

    if member:
        return True
    return False
