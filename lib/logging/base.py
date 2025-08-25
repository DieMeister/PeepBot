import datetime as dt
from datetime import datetime

from colorama import Fore
import sqlite3
from enum import Enum
from typing import Optional, Union

from discord import Interaction
from discord.ext.commands.context import Context

from lib.getter.config import log_path, datetime_format


__all__ = [
    "LogType",
    "ExecutionMethod",
    "Module",
    "CommandType",
    "default_logger",
    "command",
    "command_possible"
]


class LogType(Enum):
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    FATAL = "fatal"
    DEBUG = "debug"


class ExecutionMethod(Enum):
    SETUP = "setup"
    LOOP = "loop"
    EVENT = "event"
    COMMAND = "command"


class Module(Enum):
    BOT = "bot"
    PEEP = "peep"
    CONFIG = "config"
    EASTER_EGG = "eastregg",
    MODERATION = "mod",
    HELP = "help"


class CommandType(Enum):
    DEVELOPER = "developer"
    ADMIN = "admin",
    MANAGER = "manager",
    MEMBER = "member"


def default_logger(log_module: Module, description: str, execution_method: ExecutionMethod, log_type: LogType=LogType.INFO) -> int:
    timestamp = datetime.now(dt.UTC)
    database_time = timestamp.strftime(datetime_format())
    console_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    connection = sqlite3.connect(log_path())
    log_id = connection.execute("""
    INSERT INTO logs (timestamp, type, log_module, description, execution_method)
    VALUES (?, ?, ?, ?, ?)
    RETURNING log_id
    """, (database_time, log_type.value, log_module.value, description, execution_method.value)).fetchone()[0]
    connection.commit()
    connection.close()

    color = Fore.CYAN
    match log_type:
        case LogType.INFO:
            color = Fore.LIGHTWHITE_EX
        case LogType.WARN:
            color = Fore.MAGENTA
        case LogType.ERROR:
            color = Fore.YELLOW
        case LogType.FATAL:
            color = Fore.RED
        case LogType.DEBUG:
            color = Fore.BLUE

    print(f"{color}[{console_time}] [{log_type.value.upper():5}] [{log_module:8}] {description}{Fore.RESET}")

    return log_id


def command(log_module: Module, description: str, context: Union[Context, Interaction], command_type: CommandType, log_type: LogType=LogType.INFO) -> int:
    log_id = default_logger(log_module, description, ExecutionMethod.COMMAND, log_type)

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
    """, (log_id, guild_id, channel_id, user_id, command_type.value))
    connection.commit()
    connection.close()

    return log_id


def command_possible(log_module: Module, description: str, execution_method: ExecutionMethod, log_type: LogType, ctx: Optional[Context], command_type: Optional[CommandType]) -> int:
    if execution_method== ExecutionMethod.COMMAND:
        if ctx is None:
            raise ValueError("Missing Argument: ctx")
        if command_type is None:
            raise ValueError("Missing Argument: command_type")
        log_id = command(log_module, description, ctx, command_type, log_type)
    else:
        log_id = default_logger(log_module, description, execution_method, log_type)

    return log_id
