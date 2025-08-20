import sqlite3
from typing import Optional, TYPE_CHECKING

from lib.logging.base import command_possible
from lib.getter.config import log_path

if TYPE_CHECKING:
    from discord.ext.commands.context import Context


__all__ = [
    "extension_success",
    "extension_error"
]

def extension_success(log_module: str, description: str, execution_method: str, extension_name: str, ctx: Optional["Context"]=None) -> int:
    log_id = command_possible(log_module, description, execution_method, "info", ctx, "developer")

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO extension_success (log_id, extension_name)
    VALUES (?, ?)
    """, (log_id, extension_name))
    connection.commit()
    connection.close()

    return log_id


def extension_error(description: str, execution_method: str, extension_name: str, failure_reason: str, ctx: Optional["Context"]=None, log_type: str="error", log_module: str="bot") -> int:
    log_id = command_possible(log_module, description, execution_method, log_type, ctx, "developer")

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO extension_error (log_id, extension_name, reason)
    VALUES (?, ?, ?)
    """, (log_id, extension_name, failure_reason))
    connection.commit()
    connection.close()

    return log_id