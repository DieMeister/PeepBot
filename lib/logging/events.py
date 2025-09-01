import sqlite3
from typing import TYPE_CHECKING, Optional

from lib.getter.config import log_path
from lib.logging.base import default_logger, Module, ExecutionMethod, LogType

if TYPE_CHECKING:
    from discord import Guild, Member


__all__ = [
    "user_join",
    "guild_join",
    "member_join"
]


def user_join(user_id: int) -> int:
    log_id = default_logger(Module.BOT, "User added to Database", ExecutionMethod.EVENT, LogType.INFO)

    log_db = sqlite3.connect(log_path())
    log_db.execute("""
    INSERT INTO user_join (log_id, user_id)
    VALUES (?, ?)
    """, (log_id, user_id))
    log_db.commit()
    log_db.close()

    return log_id


def guild_join(guild: "Guild", members_added: Optional[int]=None, log_type: LogType=LogType.INFO) -> int:
    log_id = default_logger(Module.BOT, "Bot joined Guild", ExecutionMethod.EVENT, log_type)

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO guild_join (log_id, guild_id, guild_name, members_total, members_added)
    VALUES (?, ?, ?, ?, ?)
    """, (log_id, guild.id, guild.name, len(guild.members), members_added))
    connection.commit()
    connection.close()

    return log_id


def member_join(member: "Member", log_type: LogType=LogType.INFO) -> int:
    log_id = default_logger(Module.BOT, "Member added to Database", ExecutionMethod.EVENT, log_type)

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO member_join (log_id, guild_id, user_id, user_name)
    VALUES (?, ?, ?, ?)
    """, (log_id, member.guild.id, member.id, member.name))
    connection.commit()
    connection.close()

    return log_id
