import sqlite3
from typing import TYPE_CHECKING, Optional, Union

from lib.logging.base import command_possible, command
from lib.getter.config import log_path

if TYPE_CHECKING:
    from discord import Interaction
    from discord.ext.commands.context import Context

__all__ = [
    "sync_commands",
    "help_embed",
    "invalid_input"
]


def sync_commands(execution_method: str, amount: int, ctx: Optional["Context"]=None) -> int:
    log_id = command_possible("bot", "Commands synced", execution_method, "info", ctx, "developer")
    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO commands_synced (log_id, amount)
    VALUES (?, ?)
    """, (log_id, amount))
    connection.commit()
    connection.close()

    return log_id


def help_embed(help_type: str, context: Union["Context", "Interaction"], command_type: str) -> int:
    log_id = command("bot", "HelpEmbed sent", context, command_type)

    con = sqlite3.connect(log_path())
    con.execute("""
    INSERT INTO help (log_id, type)
    VALUES (?, ?)
    """, (log_id, help_type))
    con.commit()
    con.close()

    return log_id


def invalid_input(log_module: str, description: str, context: Union["Context", "Interaction"], command_type: str, given_input: str, log_type:str="info") -> int:
    log_id = command(log_module, description, context, command_type, log_type)

    con = sqlite3.connect(log_path())
    con.execute("""
    INSERT INTO invalid_input (log_id, input)
    VALUE (?, ?)
    """, (log_id, given_input))
    con.commit()
    con.close()
    return log_id
