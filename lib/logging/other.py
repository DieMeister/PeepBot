import sqlite3
from typing import TYPE_CHECKING, Optional, Union
from enum import Enum

from lib.logging import command_possible, command, Module, ExecutionMethod, LogType, CommandType
from lib.getter.config import log_path

if TYPE_CHECKING:
    from discord import Interaction
    from discord.ext.commands.context import Context

__all__ = [
    "HelpType",
    "HelpCategory",
    "sync_commands",
    "help_embed",
    "invalid_input"
]


class HelpType(Enum):
    DEVELOPER = "dev"
    CONFIG = "config"
    USAGE = "usage"


class HelpCategory(Enum):
    PEEP = "peep"
    ASSIGNABLE_ROLES = "assignable_roles"
    ALL = "all"


def sync_commands(execution_method: ExecutionMethod, amount: int, ctx: Optional["Context"]=None) -> int:
    """Log the syncing of the bot's application commands with discord.

    Return the log_id

    Parameters
    -----------
    execution_method: :class:`ExecutionMethod`
        The way this function was called.
    amount: :class:`int`
        The amount of commands that got synced.
    ctx: Union[:class:`int`, :class:`None`]=:class:`None`
        The context of the command.
    """
    log_id = command_possible(Module.BOT, "Commands synced", execution_method, LogType.INFO, ctx, CommandType.DEVELOPER)
    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO commands_synced (log_id, amount)
    VALUES (?, ?)
    """, (log_id, amount))
    connection.commit()
    connection.close()

    return log_id


def help_embed(help_type: HelpType, help_category: HelpCategory, context: Union["Context", "Interaction"], command_type: CommandType) -> int:
    """Log when help embeds are sent.

    Return the log_id.

    Parameters
    -----------
    help_type: :class:`HelpType`
        The Type of the help embed.
    help_category: :class:`HelpCategory`
        The category of the help embed.
    context: Union[:class:`Context`, :class:`Interaction]
        The context or interaction of the command.
        Prefix commands use a context while application commands create an interaction.
    command_type: :class:`CommandType`
        The type of the command used to request the help embed.
    """
    log_id = command(Module.BOT, "HelpEmbed sent", context, command_type)

    con = sqlite3.connect(log_path())
    con.execute("""
    INSERT INTO help (log_id, type, category)
    VALUES (?, ?, ?)
    """, (log_id, help_type.value, help_category.value))
    con.commit()
    con.close()

    return log_id


def invalid_input(log_module: Module, description: str, context: Union["Context", "Interaction"], command_type: CommandType, given_input: str, log_type: LogType=LogType.INFO) -> int:
    """Log when a given input is invalid.

    Return the log_id.

    Parameters
    -----------
    log_module: :class:`Module`
        The log module that called this function.
    description: :class:`str`
        A short description of what happened.
    context: Union[:class:`Context`, :class:`Interaction`]
        The context or interaction of the command where the inout comes from.
    command_type: :class:`CommandType`
        The type of the command that caused the invalid input.
    given_input: :class:`str`
        The invalid input.
    log_type: :class:`LogType`=`LogType.INFO`
        The type of log this is.
    """
    log_id = command(log_module, description, context, command_type, log_type)

    con = sqlite3.connect(log_path())
    con.execute("""
    INSERT INTO invalid_input (log_id, input)
    VALUE (?, ?)
    """, (log_id, given_input))
    con.commit()
    con.close()
    return log_id
