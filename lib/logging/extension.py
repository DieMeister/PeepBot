import sqlite3
from typing import Optional, TYPE_CHECKING

from lib import config
from lib.logging.base import command_possible

if TYPE_CHECKING:
    from discord.ext.commands.context import Context
    from lib.types import LogModule, LogType, EventTrigger


__all__ = [
    "extension_success",
    "extension_error"
]

def extension_success(log_module: "LogModule", description: str, event_trigger: "EventTrigger", extension_name: str, ctx: Optional["Context"]=None) -> int:
    """Log the successful loading, unloading, and reloading of an extension.

    Return the log_id.

    Parameters
    -----------
    log_module: :class:`str`
        The module that calls this function.
    description: :class:`str`
        A short description of what happened.
    event_trigger: :class:`str`
        The way this function was called.
    extension_name: :class:`str`
        The name of the extension.
    ctx: Optional[:class:`Context`]=:class:`None`
        The context of the command if a command was the trigger to executing this function.
    """
    log_id = command_possible(log_module, description, event_trigger, "info", ctx, "developer")

    log_db = sqlite3.connect(config.log_db_path())
    log_db.execute("""
    INSERT INTO extension_success (log_id, extension_name)
    VALUES (?, ?)
    """, (log_id, extension_name))
    log_db.commit()
    log_db.close()

    return log_id


def extension_error(description: str, event_trigger: "EventTrigger", extension_name: str, failure_reason: str, ctx: Optional["Context"]=None, log_type: "LogType"="error", log_module: "LogModule"="bot") -> int:
    """Log the failure of loading, unloading, and reloading extensions.

    Return the log_id.

    Parameters
    -----------
    description: :class:`str`
        A short description of what happened.
    event_trigger: :class:`str`
        The way this function was called.
    extension_name: :class:`str`
        The name of the extension.
    failure_reason: :class:`str`
        The reason the action performed on the extension failed.
    ctx: Optional[:class:`Context`]=:class:`None`
        the context of the command if a command was the trigger to executing this function.
    log_type: :class:`str`="error"
        The severity of the failure.
    log_module: :class:`str`="bot"
        The module that called this function.
    """
    log_id = command_possible(log_module, description, event_trigger, log_type, ctx, "developer")

    log_db = sqlite3.connect(config.log_db_path())
    log_db.execute("""
    INSERT INTO extension_error (log_id, extension_name, reason)
    VALUES (?, ?, ?)
    """, (log_id, extension_name, failure_reason))
    log_db.commit()
    log_db.close()

    return log_id