import sqlite3
from typing import TYPE_CHECKING, Optional, Union

from lib.logging import command_possible, command
from lib.getter.config import log_path

if TYPE_CHECKING:
    from discord import Interaction
    from discord.ext.commands.context import Context
    from lib.types import EventTrigger, HelpType, HelpSubType, CommandType, LogModule, LogType

__all__ = [
    "sync_commands",
    "help_embed",
    "invalid_input"
]


def sync_commands(event_trigger: "EventTrigger", amount: int, ctx: Optional["Context"]=None) -> int:
    """Log the syncing of the bot's application commands with discord.

    Return the log_id

    Parameters
    -----------
    event_trigger: :class:`str`
        The way this function was called.
    amount: :class:`int`
        The amount of commands that got synced.
    ctx: Union[:class:`int`, :class:`None`]=:class:`None`
        The context of the command.
    """
    log_id = command_possible("bot", "Commands synced", event_trigger, "info", ctx, "developer")
    log_db = sqlite3.connect(log_path())
    log_db.execute("""
    INSERT INTO commands_synced (log_id, amount)
    VALUES (?, ?)
    """, (log_id, amount))
    log_db.commit()
    log_db.close()

    return log_id


def help_embed(help_type: "HelpType", sub_type: Optional["HelpSubType"], context: Union["Context", "Interaction"], command_type: "CommandType") -> int:
    """Log when help embeds are sent.

    Return the log_id.

    Parameters
    -----------
    help_type: :class:`HelpType`
        The Type of the help embed.
    sub_type: Optional[:class:`str`]
        The sub-command if one exists.
    context: Union[:class:`Context`, :class:`Interaction]
        The context or interaction of the command.
        Prefix commands use a context while application commands create an interaction.
    command_type: :class:`str`
        The type of the command used to request the help embed.
    """
    log_id = command("bot", "HelpEmbed sent", context, command_type)

    log_db = sqlite3.connect(log_path())
    log_db.execute("""
    INSERT INTO help (log_id, type, sub_type)
    VALUES (?, ?, ?)
    """, (log_id, help_type, sub_type))
    log_db.commit()
    log_db.close()

    return log_id


def invalid_input(log_module: "LogModule", description: str, context: Union["Context", "Interaction"], command_type: "CommandType", given_input: Union[str, int], log_type: "LogType"="info") -> int:
    """Log when a given input is invalid.

    Return the log_id.

    Parameters
    -----------
    log_module: :class:`str`
        The log module that called this function.
    description: :class:`str`
        A short description of what happened.
    context: Union[:class:`Context`, :class:`Interaction`]
        The context or interaction of the command where the inout comes from.
    command_type: :class:`str`
        The type of the command that caused the invalid input.
    given_input: Union[:class:`str`, :class:`int`]
        The invalid input.
    log_type: :class:`str`="info"
        The type of log this is.
    """
    log_id = command(log_module, description, context, command_type, log_type)

    log_db = sqlite3.connect(log_path())

    if isinstance(given_input, str):
        log_db.execute("""
        INSERT INTO invalid_str_input (log_id, input)
        VALUES (?, ?)
        """, (log_id, given_input))
    elif isinstance(given_input, int):
        log_db.execute("""
        INSERT INTO invalid_int_input (log_id, input)
        VALUES (?, ?)
        """, (log_id, given_input))
    else:
        raise ValueError("given_input not of type str or int")

    log_db.commit()
    log_db.close()
    return log_id
