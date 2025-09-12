import sqlite3
from typing import  TYPE_CHECKING, Optional

from lib import config
from lib.logging.base import command

if TYPE_CHECKING:
    from discord import Interaction, TextChannel
    from lib.types import LogModule


__all__ = [
    "configure_channel",
    "change_of_assignable_roles",
    "set_log_channel",
    "change_peep_message"
]


def configure_channel(log_module: "LogModule", description: str, interaction: "Interaction", channel: "TextChannel") -> int:
    """Log when psps channel are added or removed.

    Return the log_id.

    Parameters
    -----------
    log_module: :class:`str`
        The module that called this function.
    description: :class:`str`
        A short description of what happened.
    interaction: :class:`Interaction`
        The interaction of the command.
    channel: :class:`TextChannel`
        The discord channel that is being configured.
    """
    log_id = command(log_module, description, interaction, "manager")

    connection = sqlite3.connect(config.log_db_path())
    connection.execute("""
    INSERT INTO configure_channel (log_id, channel_id, channel_name)
    VALUES (?, ?, ?)
    """, (log_id, channel.id, channel.name))
    connection.commit()
    connection.close()

    return log_id


def change_of_assignable_roles(description: str, interaction: "Interaction", role_id: int, reason: Optional[str]) -> int:
    """Log adding and removing Roles as assignable Roles and its failure.

    Return the log_id.

    Parameters
    -----------
    description: :class:`str`
        A short description of what happened.
    interaction: :class:`Interaction`
        The interaction of the used command.
    role_id: :class:`int`
        The discord id of the role.
    reason: Optional[:class:`str`]
        The reason why the role was added or removed.
    """
    log_id = command("mod", description, interaction, "admin")

    con = sqlite3.connect(config.log_db_path())
    con.execute("""
    INSERT INTO adding_role_to_list (log_id, role_id, reason)
    VALUES (?, ?, ?) 
    """, (log_id, role_id, reason))
    con.commit()
    con.close()

    return log_id


def set_log_channel(interaction: "Interaction", channel_id: int) -> int:
    """Log when a logging channel is set or changed.

    Return the log_id.

    Parameters
    -----------
    interaction: :class:`Interaction`
        The interaction of the command.
    channel_id: :class:`int`
        The discord id of the set channel.
    """
    log_id = command("mod", "New LogChannel set", interaction, "admin")
    con = sqlite3.connect(config.log_db_path())
    con.execute("""
    INSERT INTO log_channel (log_id, channel_id)
    VALUES (?, ?)
    """, (log_id, channel_id))
    return log_id


def change_peep_message(interaction: "Interaction", message_type: str, old_message: str, new_message: str) -> int:
    """Log when the content of a peep message is changed.

    Return the log_id.

    Parameters
    -----------
    interaction: :class:`Interaction`
        The interaction of the command.
    message_type: :class:`str`
        Which peep message was changed.
    old_message: :class:`str`
        The content of the old message.
    new_message: :class:`str`
        The conetent of the new message.
    """
    log_id = command("config", "PeepMessage changed", interaction, "manager")

    connection = sqlite3.connect(config.log_db_path())
    connection.execute("""
    INSERT INTO change_peep_message (log_id, message_type, old_message, new_message)
    VALUES (?, ?, ?, ?)
    """, (log_id, message_type, old_message, new_message))
    connection.commit()
    connection.close()

    return log_id
