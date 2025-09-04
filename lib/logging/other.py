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
    log_id = command(Module.BOT, "HelpEmbed sent", context, command_type)

    con = sqlite3.connect(log_path())
    con.execute("""
    INSERT INTO help (log_id, type, category)
    VALUES (?, ?, ?)
    """, (log_id, help_type.value, help_category.value))
    con.commit()
    con.close()

    return log_id


def invalid_input(log_module: Module, description: str, context: Union["Context", "Interaction"], command_type: CommandType, given_input: Union[str, int], log_type: LogType=LogType.INFO) -> int:
    log_id = command(log_module, description, context, command_type, log_type)

    con = sqlite3.connect(log_path())

    if isinstance(given_input, str):
        con.execute("""
        INSERT INTO invalid_str_input (log_id, input)
        VALUE (?, ?)
        """, (log_id, given_input))
    elif isinstance(given_input, int):
        con.execute("""
        INSERT INTO invalid_int_input (log_id, input)
        VALUE (?, ?)
        """, (log_id, given_input))
    else:
        raise ValueError("given_input not of type str or int")

    con.commit()
    con.close()
    return log_id
