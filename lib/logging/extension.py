import sqlite3
from typing import Optional, TYPE_CHECKING

from lib.logging import LogType, Module, CommandType
from lib.logging.base import command_possible
from lib.getter.config import log_path

if TYPE_CHECKING:
    from discord.ext.commands.context import Context
    from lib.logging import ExecutionMethod


__all__ = [
    "extension_success",
    "extension_error"
]

def extension_success(log_module: Module, description: str, execution_method: "ExecutionMethod", extension_name: str, ctx: Optional["Context"]=None) -> int:
    """Log the successful loading, unloading, and reloading of an extension.

    Return the log_id.

    Parameters
    -----------
    log_module: :class:`Module`
        The module that calls this function.
    description: :class:`str`
        A short description of what happened.
    execution_method: :class:`ExecutionMethod`
        The way this function was called.
    extension_name: :class:`str`
        The name of the extension.
    ctx: Optional[:class:`Context`]=:class:`None`
        The context of the command if a command was the trigger to executing this function.
    """
    log_id = command_possible(log_module, description, execution_method, LogType.INFO, ctx, CommandType.DEVELOPER)

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO extension_success (log_id, extension_name)
    VALUES (?, ?)
    """, (log_id, extension_name))
    connection.commit()
    connection.close()

    return log_id


def extension_error(description: str, execution_method: "ExecutionMethod", extension_name: str, failure_reason: str, ctx: Optional["Context"]=None, log_type: LogType=LogType.ERROR, log_module: Module=Module.BOT) -> int:
    """Log the failure of loading, unloading, and reloading extensions.

    Return the log_id.

    Parameters
    -----------
    description: :class:`str`
        A short description of what happened.
    execution_method: :class:`str`
        The way this function was called.
    extension_name: :class:`str`
        The name of the extension.
    failure_reason: :class:`str`
        The reason the action performed on the extension failed.
    ctx: Optional[:class:`Context`]=:class:`None`
        the context of the command if a command was the trigger to executing this function.
    log_type: :class:`LogType`=LogType.ERROR
        The severity of the failure.
    log_module: :class:`Module`=Module.BOT
        The module that called this function.
    """
    log_id = command_possible(log_module, description, execution_method, log_type, ctx, CommandType.DEVELOPER)

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO extension_error (log_id, extension_name, reason)
    VALUES (?, ?, ?)
    """, (log_id, extension_name, failure_reason))
    connection.commit()
    connection.close()

    return log_id