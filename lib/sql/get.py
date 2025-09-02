import sqlite3
from typing import Optional

from lib.getter.config import database_path


__all__ = [
    "get_user",
    "get_guild",
    "get_member",
    "get_channel"
]


def get_user(user_id: int) -> Optional[tuple[int, Optional[int]]]:
    data_db = sqlite3.connect(database_path())
    user = data_db.execute("""
    SELECT
        user_id,
        stolen_peeps
    FROM users
    WHERE user_id = ?
    """, (user_id,)).fetchone()
    data_db.close()
    return user


def get_guild(guild_id: int) -> Optional[tuple[int, str, str, str, str, int]]:
    con = sqlite3.connect(database_path())
    guild = con.execute("""
        SELECT *
        FROM guilds
        WHERE guild_id = ?
        """, (guild_id,)).fetchone()
    con.close()
    return guild


def get_member(guild_id: int, user_id: int) -> Optional[tuple[int, int, str, int, int, int, int]]:
    con = sqlite3.connect(database_path())
    member = con.execute("""
        SELECT *
        FROM members
        WHERE guild_id = ?
        AND user_id = ?
        """, (guild_id, user_id)).fetchone()
    con.close()
    return member


def get_channel(channel_id: int) -> Optional[tuple[int, int]]:
    con = sqlite3.connect(database_path())
    channel = con.execute("""
    SELECT *
    FROM allowed_channels
    WHERE channel_id = ?
    """, (channel_id,)).fetchone()
    con.close()
    return channel