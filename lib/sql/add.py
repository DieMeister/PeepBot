import sqlite3
from typing import TYPE_CHECKING

import datetime as dt
from datetime import datetime

from lib.getter.config import database_path
from lib.getter.date_time import dt_string, now
from lib.sql.get import get_guild, get_member, get_user
from lib import logging

if TYPE_CHECKING:
    from discord import Guild, Member


__all__ = [
    "add_guild",
    "add_member"
]


# TODO return lib.types.sql.User
def _add_user(user_id: int) -> None:
    if get_user(user_id) is None:
        data_db = sqlite3.connect(database_path())
        data_db.execute("""
        INSERT INTO users (user_id)
        VALUES (?)
        """, (user_id,))
        data_db.commit()
        data_db.close()
        logging.user_join(user_id)


# TODO return lib.types.sql.Guild
def add_guild(guild: "Guild") -> None:
    """Add guild to database if it is not in it already.

    Parameters
    -----------
    guild: :class:`Guild`
        the guild that is being added.
    """
    if get_guild(guild.id) is None:
        con = sqlite3.connect(database_path())
        con.execute("""
        INSERT INTO guilds (guild_id, last_peep)
        VALUES (?, ?)
        """, (guild.id, dt_string(now())))
        con.commit()
        con.close()
        logging.guild_join(guild)


# TODO return lib.types.sql.Member
def add_member(member: "Member"):
    """Add member to database if they are not in it already.

    Parameters
    -----------
    member: :class:`Member`
        The member that is being added.
    """
    if get_member(member.guild.id, member.id) is None:
        add_guild(member.guild)
        _add_user(member.id)
        con = sqlite3.connect(database_path())
        con.execute("""
        INSERT INTO members (
            user_id,
            guild_id,
            last_peep
        )
        VALUES (?, ?, ?)
        """, (member.id, member.guild.id, dt_string(now())))
        con.commit()
        con.close()
        logging.member_join(member)
