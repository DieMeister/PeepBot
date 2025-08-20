import sqlite3
from typing import TYPE_CHECKING

from lib.getter.config import log_path
from lib.logging.base import default_logger

if TYPE_CHECKING:
    from discord import Guild, Member


__all__ = [
    "guild_join",
    "member_join"
]


def guild_join(guild: "Guild", members_added: int, log_type: str="info") -> int:
    log_id = default_logger("bot", "Bot joined Guild", "event", log_type)

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO guild_join (log_id, guild_id, guild_name, members_added, members_total)
    VALUES (?, ?, ?, ?, ?)
    """, (log_id, guild.id, guild.name, members_added, len(guild.members)))
    connection.commit()
    connection.close()

    return log_id


def member_join(member: "Member", log_type: str="info") -> int:
    log_id = default_logger("bot", "Member joined Guild", "event", log_type)

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO member_join (log_id, guild_id, user_id, user_name)
    VALUES (?, ?, ?, ?)
    """, (log_id, member.guild.id, member.id, member.name))
    connection.commit()
    connection.close()

    return log_id
