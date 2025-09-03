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
    """Fetch a user from the database.Return :class:`None` if the user is not found.

    Parameters
    -----------
    user_id: :class:`int`
        the discord id of the user.
    """
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
    """Fetch a guild from the database. Return :class:`None` if the guild is not found.

    Parameters
    -----------
    guild_id: :class:`int`
        The discord id of the guild.
    """
    con = sqlite3.connect(database_path())
    guild = con.execute("""
        SELECT *
        FROM guilds
        WHERE guild_id = ?
        """, (guild_id,)).fetchone()
    con.close()
    return guild


def get_member(guild_id: int, user_id: int) -> Optional[tuple[int, int, str, int, int, int, int]]:
    """Fetch a member from the database. Return :class:`None` if the member is not found.

    Parameters
    -----------
    guild_id: :class:`int`
        The discord id of the guild the member is part of.
    user_id: :class:`int`
        The discord id of the user the member represents in this guild.
    """
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
    """Fetch an AllowedChannel from the database. Return :class:`None` if the channel is not found.

    Parameters
    -----------
    channel_id: :class:`int`
        The discord id of the channel.
    """
    con = sqlite3.connect(database_path())
    channel = con.execute("""
    SELECT *
    FROM allowed_channels
    WHERE channel_id = ?
    """, (channel_id,)).fetchone()
    con.close()
    return channel