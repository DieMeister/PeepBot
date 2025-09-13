import datetime as dt
from datetime import datetime

from discord import Interaction
from discord.ext.commands.context import Context

import sqlite3
from colorama import Fore
from typing import Optional, Union, TYPE_CHECKING
from lib import config

if TYPE_CHECKING:
    from lib.types import LogType, EventTrigger, LogModule, CommandType

__all__ = [
    "default_logger",
    "command",
    "command_possible"
]


def default_logger(log_module: "LogModule", description: str, event_trigger: "EventTrigger", log_type: LogType= "info") -> int:
    """Default logger, is called by every other logger function.

    Return the log_id.

    Parameters
    -----------
    log_module: :class:`str`
        The module that called a log function.
    description: :class:`str`
        A short description of what happened.
    event_trigger: :class:`str`
        The way the event was triggered.
    log_type: :class:`str`
        The severity of the event.
    """
    timestamp = datetime.now(dt.UTC)
    database_time = timestamp.strftime(config.discord_dt_format())
    console_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    log_db = sqlite3.connect(config.log_db_path())
    log_id = log_db.execute("""
    INSERT INTO logs (timestamp, type, log_module, description, execution_method)
    VALUES (?, ?, ?, ?, ?)
    RETURNING log_id
    """, (database_time, log_type, log_module, description, event_trigger)).fetchone()[0]
    log_db.commit()
    log_db.close()

    match log_type:
        case "info":
            color = Fore.LIGHTWHITE_EX
        case "warn":
            color = Fore.MAGENTA
        case "error":
            color = Fore.YELLOW
        case "fatal":
            color = Fore.RED
        case "debug":
            color = Fore.BLUE
        case _:
            color = Fore.CYAN

    print(f"{color}[{console_time}] [{log_type.upper():5}] [{log_module.upper():8}] {description}{Fore.RESET}")

    return log_id


def command(log_module: "LogModule", description: str, context: Union[Context, Interaction], command_type: "CommandType", log_type: "LogType"="info") -> int:
    """Base logger for all commands. This is called whenever a command is involved.

    Return the log_id.

    Parameters
    -----------
    log_module: :class:`str`
        The module that called a log function.
    description: :class:`str`
        A short description of what happened.
    context: Union[:class:`Context`, :class:`Interaction`]
        The context or interaction of the command.
    command_type: :class:`str`
        Who is allowed to use the command.
    log_type: :class:`str`
        The severity of the event.
    """
    log_id = default_logger(log_module, description, "command", log_type)

    guild_id = context.guild.id
    channel_id = context.channel.id
    if isinstance(context, Context):
        user_id = context.author.id
        prefix = context.prefix
    elif isinstance(context, Interaction):
        user_id = context.user.id
        prefix = None
    else:
        raise ValueError("command context not of type Context or Interaction")

    log_db = sqlite3.connect(config.log_db_path())
    log_db.execute("""
    INSERT INTO commands (log_id, guild_id, channel_id, user_id, type, prefix)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (log_id, guild_id, channel_id, user_id, command_type, prefix))
    log_db.commit()
    log_db.close()

    return log_id


def command_possible(log_module: "LogModule", description: str, event_trigger: "EventTrigger", log_type: "LogType", ctx: Optional[Context], command_type: Optional["CommandType"]) -> int:
    """Log when a command is a possible trigger but not necessary.

    This function calls either :func:`base_logger` or :func:`command` depending on if a command is involved.
    Return the log_id.

    Parameters
    -----------
    log_module: :class:`str`
        The module that called a log function.
    description: :class:`str`
        A short description of what happened.
    event_trigger: :class:`str`
        The trigger of the event. If a command is involved this is ExecutionMethod.COMMAND
    ctx: :class:`Context`
        The context or interaction of the command.
    log_type: :class:`str`
        The severity of the event.
    command_type: :class:`str`
        Who is allowed to use the command.
    """

    if event_trigger == "command":
        if ctx is None:
            raise ValueError("Missing Argument: ctx")
        if command_type is None:
            raise ValueError("Missing Argument: command_type")
        log_id = command(log_module, description, ctx, command_type, log_type)
    else:
        log_id = default_logger(log_module, description, event_trigger, log_type)

    return log_id
