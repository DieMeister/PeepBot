from typing import TypedDict


__all__ = [
    "data",
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
    "date_time",
    "database_query",
    "log_query",
    "log_channel_missing"
]


class Thief(TypedDict):
    name: str
    emote: str
    id: int


data: dict

def developer() -> list[int]:
    return data["people"]["developer"]


def vip() -> list[int]:
    return data["people"]["vip"]


def vup() -> list[int]:
    return data["people"]["vup"]


def thieves() -> list[Thief]:
    return data["emotes"]["thieves"]


def gifted_emote() -> str:
    return data["emotes"]["leaderboard"]["gifted"]


def peeps_emote() -> str:
    return data["emotes"]["leaderboard"]["peeps"]


def received_emote() -> str:
    return data["emotes"]["leaderboard"]["received"]


def tries_emote() -> str:
    return data["emotes"]["leaderboard"]["tries"]


def embed_color() -> int:
    return data["embed_color"]


def database_path() -> str:
    return data["file_paths"]["database"]


def database_backup_path() -> str:
    return data["file_paths"]["database_saves"]


def log_path() -> str:
    return data["file_paths"]["logs"]


def dt_format() -> str:
    return data["datetime_formats"]["datetime"]


def discord_dt_format() -> str:
    return data["datetime_formats"]["discord"]


def date_format() -> str:
    return data["datetime_formats"]["date"]


def database_query() -> str:
    return data["sql_table_queries"]["database"]


def log_query() -> str:
    return data["sql_table_queries"]["logs"]


def log_channel_missing() -> str:
    return data["messages"]["log_channel_missing"]
