import sqlite3
from typing import TYPE_CHECKING

from lib.getter.config import database_path
from lib.getter.date_time import dt_string

if TYPE_CHECKING:
    from datetime import datetime
    from discord import Guild


__all__ = [
    "add_members",
    "add_member",
    "add_guild"
]

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
    con.commit()
    con.close()
    return len(members_data)


def add_guild(guild: "Guild", timestamp: "datetime") -> int:
    con = sqlite3.connect(database_path())
    con.execute("""
    INSERT INTO guilds (guild_id, last_peep)
    VALUES (?, ?)
    """, (guild.id, dt_string(timestamp)))
    con.commit()
    con.close()

    members = []
    for member in guild.members:
        members.append(
            (
                member.id,
                guild.id,
                dt_string(timestamp)
            )
        )
    return add_members(members)


def add_member(user_id: int, guild_id: int, timestamp: "datetime"):
    con = sqlite3.connect(database_path())
    con.execute("""
    INSERT INTO members (
        user_id,
        guild_id,
        last_peep
    )
    VALUES (?, ?, ?)
    """, (user_id, guild_id, dt_string(timestamp)))
    con.commit()
    con.close()