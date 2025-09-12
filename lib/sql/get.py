import sqlite3
from typing import Optional, TYPE_CHECKING
from lib import config

if TYPE_CHECKING:
    from lib import types


__all__ = [
    "get_user",
    "get_guild",
    "get_member",
    "get_psps_channel"
]


def get_user(user_id: int) -> Optional["types.sql.User"]:
    """Fetch a user from the database.Return :class:`None` if the user is not found.

    Parameters
    -----------
    user_id: :class:`int`
        the discord id of the user.
    """
    data_db = sqlite3.connect(config.data_db_path())
    user: Optional["types.sql.User"] = data_db.execute("""
    SELECT
        user_id,
        stolen_peeps
    FROM users
    WHERE user_id = ?
    """, (user_id,)).fetchone()
    data_db.close()
    return user


def get_guild(guild_id: int) -> Optional["types.sql.Guild"]:
    """Fetch a guild from the database. Return :class:`None` if the guild is not found.

    Parameters
    -----------
    guild_id: :class:`int`
        The discord id of the guild.
    """
    data_db = sqlite3.connect(config.data_db_path())
    guild: Optional["types.sql.Guild"] = data_db.execute("""
        SELECT 
            guild_id,
            success_message,
            scratch_message,
            no_peep_message,
            last_peep,
            log_channel_id
        FROM guilds
        WHERE guild_id = ?
        """, (guild_id,)).fetchone()
    data_db.close()
    return guild


def get_member(guild_id: int, user_id: int) -> Optional["types.sql.Member"]:
    """Fetch a member from the database. Return :class:`None` if the member is not found.

    Parameters
    -----------
    guild_id: :class:`int`
        The discord id of the guild the member is part of.
    user_id: :class:`int`
        The discord id of the user the member represents in this guild.
    """
    data_db = sqlite3.connect(config.data_db_path())
    member: Optional["types.sql.Member"] = data_db.execute("""
        SELECT 
            user_id,
            guild_id,
            last_peep,
            caught_peeps,
            tries,
            sent_peeps,
            received_peeps
        FROM members
        WHERE guild_id = ?
        AND user_id = ?
        """, (guild_id, user_id)).fetchone()
    data_db.close()
    return member


def get_psps_channel(channel_id: int) -> Optional["types.sql.PspsChannel"]:
    """Fetch an AllowedChannel from the database. Return :class:`None` if the channel is not found.

    Parameters
    -----------
    channel_id: :class:`int`
        The discord id of the channel.
    """
    con = sqlite3.connect(config.data_db_path())
    channel: "types.sql.PspsChannel" = con.execute("""
    SELECT 
        channel_id,
        guild_id
    FROM allowed_channels
    WHERE channel_id = ?
    """, (channel_id,)).fetchone()
    con.close()
    return channel