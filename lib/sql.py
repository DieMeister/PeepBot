import sqlite3
from typing import TYPE_CHECKING, Optional

import discord

from .getter import database_path
from .date_time import get_datetime_string

if TYPE_CHECKING:
    from datetime import datetime
    from discord import Guild


__all__ = [
    "get_guild",
    "get_member",
    "get_channel",
    "add_guild",
    "add_member",
    "add_members"
]


def get_guild(guild_id: int) -> Optional[tuple[int, str, str, str, str]]:
    con = sqlite3.connect(database_path())
    guild = con.execute("""
        SELECT *
        FROM guilds
        WHERE guild_id = ?
        """, (guild_id,)).fetchone()
    con.close()
    return guild


def get_member(guild_id: int, user_id: int) -> Optional[tuple[int, int, str, int, int]]:
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
    con = sqlite3.connect(database_path())
    channel = con.execute("""
    SELECT *
    FROM allowed_channels
    WHERE channel_id = ?
    """, (channel_id,)).fetchone()
    con.close()
    return channel


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


def add_guild(guild: Guild, timestamp: "datetime") -> int:
    con = sqlite3.connect(database_path())
    con.execute("""
    INSERT INTO guilds (guild_id, last_peep)
    VALUES (?, ?)
    """, (guild.id, get_datetime_string(timestamp)))
    con.close()

    members = []
    for member in guild.members:
        members.append(
            (
                member.id,
                guild.id,
                get_datetime_string(timestamp)
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
    """, (user_id, guild_id, get_datetime_string(timestamp)))
