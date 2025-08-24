import sqlite3
from typing import TYPE_CHECKING

import datetime as dt
from datetime import datetime

from lib.getter.config import database_path
from lib.getter.date_time import dt_string
from lib.sql.get import get_guild, get_member
from lib import logging

if TYPE_CHECKING:
    from discord import Guild, Member


__all__ = [
    "add_member",
    "add_guild"
]


def add_guild(guild: "Guild") -> None:
    if get_guild(guild.id) is None:
        con = sqlite3.connect(database_path())
        con.execute("""
        INSERT INTO guilds (guild_id, last_peep)
        VALUES (?, ?)
        """, (guild.id, datetime.now(dt.UTC)))
        con.commit()
        con.close()
        logging.guild_join(guild)


def add_member(member: "Member"):
    if get_member(member.guild.id, member.id) is None:
        if get_guild(member.guild.id) is None:
            add_guild(member.guild)
        con = sqlite3.connect(database_path())
        con.execute("""
        INSERT INTO members (
            user_id,
            guild_id,
            last_peep
        )
        VALUES (?, ?, ?)
        """, (member.id, member.guild.id, dt_string(datetime.now(dt.UTC))))
        con.commit()
        con.close()
        logging.member_join(member)

