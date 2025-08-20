import datetime as dt
from datetime import datetime

from colorama import Fore
import sqlite3
from typing import Optional, Union

from discord import Interaction
from discord.ext.commands.context import Context

from lib.getter.config import log_path, datetime_format


__all__ = [
    "default_logger",
    "command",
    "command_possible"
]


def default_logger(log_module: str, description: str, execution_method: str, log_type: str="info") -> int:
    timestamp = datetime.now(dt.UTC)
    database_time = timestamp.strftime(datetime_format())
    console_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    colors = {
        "info": Fore.LIGHTWHITE_EX,
        "warn": Fore.MAGENTA,
        "error": Fore.YELLOW,
        "fatal": Fore.RED,
        "debug": Fore.BLUE
    }
    execution_methods = [
        "setup",
        "loop",
        "event",
        "command"
    ]
    modules = [
        "bot",
        "peep",
        "config",
        "eastregg",
        "mod",
        "help"
    ]

    if log_type not in colors:
        raise ValueError("Provided LoggingType does not exist")
    if log_module not in modules:
        raise ValueError("Provided LoggingModule does not exist")
    if execution_method not in execution_methods:
        raise ValueError("Provided ExecutionMethod does not exist")

    connection = sqlite3.connect(log_path())
    log_id = connection.execute("""
    INSERT INTO logs (timestamp, type, log_module, description, execution_method)
    VALUES (?, ?, ?, ?, ?)
    RETURNING log_id
    """, (database_time, log_type, log_module, description, execution_method)).fetchone()[0]
    connection.commit()
    connection.close()

    color = colors[log_type]

    print(f"{color}[{console_time}] [{log_type.upper():5}] [{log_module:8}] {description}{Fore.RESET}")

    return log_id


def command(log_module: str, description: str, context: Union[Context, Interaction], command_type: str, log_type: str="info") -> int:
    command_types = [
        "developer",
        "admin",
        "manager",
        "member"
    ]
    if command_type not in command_types:
        raise ValueError("Provided CommandType does not exit")

    log_id = default_logger(log_module, description, "command", log_type)

    guild_id = context.guild.id
    channel_id = context.channel.id
    if isinstance(context, Context):
        user_id = context.author.id
    elif isinstance(context, Interaction):
        user_id = context.user.id
    else:
        raise ValueError("command context not of type Context or Interaction")

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO commands (log_id, guild_id, channel_id, user_id, type)
    VALUES (?, ?, ?, ?, ?)
    """, (log_id, guild_id, channel_id, user_id, command_type))
    connection.commit()
    connection.close()

    return log_id


def command_possible(log_module: str, description: str, execution_method: str, log_type: str, ctx: Optional[Context], command_type: str) -> int:
    if execution_method == "command":
        if ctx is None:
            raise ValueError("Missing Argument: ctx")
        if command_type is None:
            raise ValueError("Missing Argument: command_type")
        log_id = command(log_module, description, ctx, command_type, log_type)
    else:
        log_id = default_logger(log_module, description, execution_method, log_type)

    return log_id
