import sqlite3
from typing import TYPE_CHECKING, Optional, Union

from lib.getter.config import database_path

if TYPE_CHECKING:
    from discord import Guild, TextChannel, StageChannel, ForumChannel, VoiceChannel, CategoryChannel


__all__ = [
    "log_channel"
]


def log_channel(guild: "Guild") -> Optional[Union["TextChannel", "StageChannel", "ForumChannel", "VoiceChannel", "CategoryChannel"]]:
    """
    Return the log channel of a guild.

    If the guild has no channel set or the channel does not exist anymore, None is returned.

    Parameters
    -----------
    guild: :class:`Guild`
        The guild whose log channel is got.
    """
    con = sqlite3.connect(database_path())
    guild_data = con.execute("""
    SELECT log_channel_id
    FROM guilds
    WHERE guild_id = ?
    """, (guild.id,)).fetchone()
    con.close()

    if guild_data is None:
        return None

    channel_id = guild_data[0]
    if channel_id is None:
        return None
    return guild.get_channel(channel_id)
