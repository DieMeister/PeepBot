from typing import TypedDict

from lib.data import json


__all__ = [
    "load_data",
    "developer",
    "vip",
    "vup",
    "thieves",
    "gifted_emote",
    "peeps_emote",
    "received_emote",
    "tries_emote",
    "embed_color",
    "database_path",
    "database_backup_path",
    "log_path",
    "dt_format",
    "discord_dt_format",
    "date_format",
    "database_query",
    "log_query",
    "log_channel_missing"
]


class Thief(TypedDict):
    name: str
    emote: str
    id: int


data: dict


def load_data(file_path: str) -> None:
    """Load the config file."""
    global data
    data = json.load_data(file_path)


def developer() -> list[int]:
    """Return the discord ids of the developers."""
    return data["people"]["developer"]


def vip() -> list[int]:
    """Return the discord ids of the very important people."""
    return data["people"]["vip"]


def vup() -> list[int]:
    """Return the discord ids of the very unimportant people."""
    return data["people"]["vup"]


def thieves() -> list[Thief]:
    """Return the discord ids of the thieves."""
    return data["people"]["thieves"]


def gifted_emote() -> str:
    """Return the markdown of the discord emote that represents gifted peeps."""
    return data["emotes"]["leaderboard"]["gifted"]


def peeps_emote() -> str:
    """Return the markdown of the discord emote that represents caught peeps."""
    return data["emotes"]["leaderboard"]["peeps"]


def received_emote() -> str:
    """Return the markdown of the discord emote that represents received peeps."""
    return data["emotes"]["leaderboard"]["received"]


def tries_emote() -> str:
    """Return the markdown of the discord emote that represents the tris to catch peeps."""
    return data["emotes"]["leaderboard"]["tries"]


def embed_color() -> int:
    """Return the color of embeds sent by the bot."""
    return data["embed_color"]


def database_path() -> str:
    """Return the filepath of the bot's database."""
    return data["file_paths"]["database"]


def database_backup_path() -> str:
    """Return the filepath of the folder to save database backups."""
    return data["file_paths"]["database_saves"]


def log_path() -> str:
    """Return the filepath of the bot's logging database."""
    return data["file_paths"]["logs"]


def dt_format() -> str:
    """Return the format for the bot's string representation of datetime objects."""
    return data["datetime_formats"]["datetime"]


def discord_dt_format() -> str:
    """Return the format for discord's string representation of datetime objects."""
    return data["datetime_formats"]["discord"]


def date_format() -> str:
    return data["datetime_formats"]["date"]


def database_query() -> str:
    """Return the query to create the bot's database."""
    return data["sql_table_queries"]["database"]


def log_query() -> str:
    """Return the sql query to create the bot's logging database."""
    return data["sql_table_queries"]["logs"]


def log_channel_missing() -> str:
    """Return the message to send when a guild's logging channel is missing."""
    return data["messages"]["log_channel_missing"]
