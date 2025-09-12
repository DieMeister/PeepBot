import sqlite3
from typing import TYPE_CHECKING, Optional

from lib import config
from lib.logging.base import default_logger

if TYPE_CHECKING:
    from discord import Guild, Member
    from lib.types import LogType


__all__ = [
    "user_join",
    "guild_join",
    "member_join"
]


def user_join(user_id: int) -> int:
    """Log when a user is added to the database.

    Return the log_id.

    Parameters
    -----------
    user_id: :class:`int`
        The discord id of the user.
    """
    log_id = default_logger("bot", "User added to Database", "event", "info")

    log_db = sqlite3.connect(config.log_db_path())
    log_db.execute("""
    INSERT INTO user_join (log_id, user_id)
    VALUES (?, ?)
    """, (log_id, user_id))
    log_db.commit()
    log_db.close()

    return log_id


def guild_join(guild: "Guild", members_added: Optional[int]=None, log_type: "LogType"="info") -> int:
    """Log when a guild is added to the database.

    Return the log_id.

    Parameters
    -----------
    guild: :class:`Guild`
        The guild that is being added.
    members_added: Optional[:class:`int`]
        The amount of members of that guild that are being added bcause the guild was added.
        This should always be None, it is only kept for compatibility reasons.
    log_type: :class:`str`="info"
        The severity of the event.
    """
    log_id = default_logger("bot", "Bot joined Guild", "event", log_type)

    log_db = sqlite3.connect(config.log_db_path())
    log_db.execute("""
    INSERT INTO guild_join (log_id, guild_id, guild_name, members_total, members_added)
    VALUES (?, ?, ?, ?, ?)
    """, (log_id, guild.id, guild.name, len(guild.members), members_added))
    log_db.commit()
    log_db.close()

    return log_id


def member_join(member: "Member", log_type: "LogType"="info") -> int:
    """Log when a member is added to the database.

    Return the log_id.

    Parameters
    -----------
    member: :class:`Member`
        The member that is being added.
    log_type: :class:`str`="info"
        The severity of the event.
    """
    log_id = default_logger("bot", "Member added to Database", "event", log_type)

    log_db = sqlite3.connect(config.log_db_path())
    log_db.execute("""
    INSERT INTO member_join (log_id, guild_id, user_id, user_name)
    VALUES (?, ?, ?, ?)
    """, (log_id, member.guild.id, member.id, member.name))
    log_db.commit()
    log_db.close()

    return log_id
