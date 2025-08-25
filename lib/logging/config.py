import sqlite3
from typing import  TYPE_CHECKING, Optional

from lib.logging import Module, CommandType
from lib.logging.base import command
from lib.getter.config import log_path

if TYPE_CHECKING:
    from discord import Interaction, TextChannel


__all__ = [
    "configure_channel",
    "change_of_assignable_roles",
    "set_log_channel",
    "change_peep_message"
]


def configure_channel(log_module: Module, description: str, interaction: "Interaction", channel: "TextChannel") -> int:
    log_id = command(log_module, description, interaction, CommandType.MANAGER)

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO configure_channel (log_id, channel_id, channel_name)
    VALUES (?, ?, ?)
    """, (log_id, channel.id, channel.name))
    connection.commit()
    connection.close()

    return log_id


def change_of_assignable_roles(description: str, interaction: "Interaction", role_id: int, reason: Optional[str]) -> int:
    log_id = command(Module.MODERATION, description, interaction, CommandType.ADMIN)

    con = sqlite3.connect(log_path())
    con.execute("""
    INSERT INTO adding_role_to_list (log_id, role_id, reason)
    VALUES (?, ?, ?) 
    """, (log_id, role_id, reason))
    con.commit()
    con.close()

    return log_id


def set_log_channel(interaction: "Interaction", channel_id: int) -> int:
    log_id = command(Module.MODERATION, "New LogChannel set", interaction, CommandType.ADMIN)
    con = sqlite3.connect(log_path())
    con.execute("""
    INSERT INTO log_channel (log_id, channel_id)
    VALUES (?, ?)
    """, (log_id, channel_id))
    return log_id


def change_peep_message(interaction: "Interaction", message_type: str, old_message: str, new_message: str) -> int:
    log_id = command(Module.CONFIG, "PeepMessage changed", interaction, CommandType.MANAGER)

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO change_peep_message (log_id, message_type, old_message, new_message)
    VALUES (?, ?, ?, ?)
    """, (log_id, message_type, old_message, new_message))
    connection.commit()
    connection.close()

    return log_id
