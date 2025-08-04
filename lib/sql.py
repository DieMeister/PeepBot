import sqlite3
from typing import TYPE_CHECKING

from .getter import database_path
from .date_time import get_datetime_string

if TYPE_CHECKING:
    from datetime import datetime


__all__ = [
    "add_guild",
    "add_member",
    "add_members"
]


def add_guild(guild_id: int, timestamp: "datetime") -> None:
    con = sqlite3.connect(database_path())
    con.execute("""
    INSERT INTO guilds (guild_id, last_peep)
    VALUES (?, ?)
    """, (guild_id, get_datetime_string(timestamp)))
    con.close()


def add_member(user_id: int, guild_id: int, timestamp: "datetime"):
    con = sqlite3.connect(database_path())
    con.execute("""
    INSERT INTO members (
        user_id,
        guild_id,
        last_peep
    )
    VALUES (?, ?, ?)
    """, (user_id, guild_id, get_datetime_string(timestamp)))


def add_members(members_data: list[tuple[int, int, str]]) -> int:
    con = sqlite3.connect(database_path())
    con.executemany("""
    INSERT INTO members (
        user_id,
        guild_id,
        last_peep
    )
    VALUES (?, ?, ?)
    """, members_data)
    con.close()
    return len(members_data)
