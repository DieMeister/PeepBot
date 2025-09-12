from typing import TypedDict, Literal


__all__ = [
    "DatabasePaths",
    "BackupPaths",
    "TableCreationPaths",
    "SqlPaths",
    "FilePaths",
    "DatetimeFormats",
    "EmoteName",
    "EmoteMarkdown",
    "Emotes",
    "Messages",
    "Thief",
    "People",
    "ConfigFile"
]


class DatabasePaths(TypedDict):
    data: str
    log: str


class BackupPaths(TypedDict):
    data_db: str


class TableCreationPaths(TypedDict):
    data: str
    log: str


class SqlPaths(TypedDict):
    table_creation: TableCreationPaths


class FilePaths(TypedDict):
    databases: DatabasePaths
    backups: BackupPaths
    sql_queries: SqlPaths


class DatetimeFormats(TypedDict):
    datetime: str
    date: str
    discord: str


type EmoteName = Literal[
    "raccoon",
    "jas",
    "creed",
    "wass",
    "moonie",
    "funne",
    "gifted",
    "peeps",
    "received",
    "tries"
]
type EmoteMarkdown = Literal[
    "<a:raccoon:1401667590316757145>",
    "<:jas:1401671986626695178>",
    "<:creed:1402701947512946789>",
    "<:wass:1402701975367188581>",
    "<:moonie:1402790093353390210>",
    "<:funne:1410555163252363284>",
    "<:gifted:1410564494869925999>",
    "<:peeps:1410564594094702593>",
    "<:received:1410564653863403580>",
    "<:tries:1410564740052418560>"
]


class Messages(TypedDict):
    log_channel_missing: str


class Thief(TypedDict):
    name: str
    emote: str
    id: int


class People(TypedDict):
    developer: list[int]
    vip: list[int]
    vup: list[int]
    thieves: list[Thief]


class ConfigFile(TypedDict):
    version: str
    embed_color: int
    file_paths: FilePaths
    datetime_formats: DatetimeFormats
    emotes: dict[EmoteName, EmoteMarkdown]
    messages: Messages
    people: People
