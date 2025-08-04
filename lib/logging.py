import datetime as dt
from datetime import datetime

from colorama import Fore
import sqlite3
from typing import TYPE_CHECKING, Optional, Union

from discord import Interaction
from discord.ext.commands.context import Context

from .getter import log_path, datetime_format

if TYPE_CHECKING:
    import discord

__all__ = [
    "default_logger",
    "command",
    "extension_success",
    "extension_error",
    "sync_commands",
    "guild_join",
    "member_join",
    "configure_channel",
    "catch_peep",
    "psps_denied",
    "change_peep_message",
    "help_embed"
]

def default_logger(log_module: str, description: str, execution_method: str, log_type: str="info") -> int:
    timestamp = datetime.now(dt.UTC)
    database_time = timestamp.strftime(datetime_format())
    console_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    colors = {
        "info": Fore.LIGHTWHITE_EX,
        "warn": Fore.MAGENTA,
        "error": Fore.YELLOW,
        "fatal": Fore.RED,
        "debug": Fore.BLUE
    }
    execution_methods = [
        "setup",
        "loop",
        "event",
        "command"
    ]
    modules = [
        "bot",
        "peep",
        "config",
        "eastregg"
    ]

    if log_type not in colors:
        raise ValueError("Provided LoggingType does not exist")
    if log_module not in modules:
        raise ValueError("Provided LoggingModule does not exist")
    if execution_method not in execution_methods:
        raise ValueError("Provided ExecutionMethod does not exist")

    connection = sqlite3.connect(log_path())
    log_id = connection.execute("""
    INSERT INTO logs (timestamp, type, log_module, description, execution_method)
    VALUES (?, ?, ?, ?, ?)
    RETURNING log_id
    """, (database_time, log_type, log_module, description, execution_method)).fetchone()[0]
    connection.commit()
    connection.close()

    color = colors[log_type]

    print(f"{color}[{console_time}] [{log_type.upper():5}] [{log_module:8}] {description}{Fore.RESET}")

    return log_id


def command(log_module: str, description: str, context: Union[Context, Interaction], command_type: str, log_type: str="info") -> int:
    command_types = [
        "developer",
        "manager",
        "member"
    ]
    if command_type not in command_types:
        raise ValueError("Provided CommandType does not exit")

    log_id = default_logger(log_module, description, "command", log_type)

    guild_id = context.guild.id
    channel_id = context.channel.id
    if isinstance(context, Context):
        user_id = context.author.id
    elif isinstance(context, Interaction):
        user_id = context.user.id
    else:
        raise ValueError("command context not of type Context or Interaction")

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO commands (log_id, guild_id, channel_id, user_id, type)
    VALUES (?, ?, ?, ?, ?)
    """, (log_id, guild_id, channel_id, user_id, command_type))
    connection.commit()
    connection.close()

    return log_id


def command_possible(log_module: str, description: str, execution_method: str, log_type: str, ctx: Optional[Context], command_type: str) -> int:
    if execution_method == "command":
        if ctx is None:
            raise ValueError("Missing Argument: ctx")
        if command_type is None:
            raise ValueError("Missing Argument: command_type")
        log_id = command(log_module, description, ctx, command_type, log_type)
    else:
        log_id = default_logger(log_module, description, execution_method, log_type)

    return log_id


def extension_success(log_module: str, description: str, execution_method: str, extension_name: str, ctx: Optional[Context]=None) -> int:
    log_id = command_possible(log_module, description, execution_method, "info", ctx, "developer")

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO extension_success (log_id, extension_name)
    VALUES (?, ?)
    """, (log_id, extension_name))
    connection.commit()
    connection.close()

    return log_id


def extension_error(description: str, execution_method: str, extension_name: str, failure_reason: str, ctx: Optional[Context]=None, log_type: str="error", log_module: str="bot") -> int:
    log_id = command_possible(log_module, description, execution_method, log_type, ctx, "developer")

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO extension_error (log_id, extension_name, reason)
    VALUES (?, ?, ?)
    """, (log_id, extension_name, failure_reason))
    connection.commit()
    connection.close()

    return log_id


def sync_commands(execution_method: str, amount: int, ctx: Optional[Context]=None) -> int:
    log_id = command_possible("bot", "Commands synced", execution_method, "info", ctx, "developer")
    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO commands_synced (log_id, amount)
    VALUES (?, ?)
    """, (log_id, amount))
    connection.commit()
    connection.close()

    return log_id


def guild_join(guild: "discord.Guild", members_added: int) -> int:
    log_id = default_logger("bot", "Bot joined Guild", "event")

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO guild_join (log_id, guild_id, guild_name, members_added, members_total)
    VALUES (?, ?, ?)
    """, (log_id, guild.id, guild.name, members_added, len(guild.members)))
    connection.commit()
    connection.close()

    return log_id


def member_join(member: "discord.Member") -> int:
    log_id = default_logger("bot", "Member joined Guild", "event")

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO member_join (log_id, guild_id, user_id, user_name)
    VALUES (?, ?, ?, ?)
    """, (log_id, member.guild.id, member.id, member.name))
    connection.commit()
    connection.close()

    return log_id


def configure_channel(log_module: str, description: str, channel: "discord.TextChannel") -> int:
    log_id = default_logger(log_module, description, "command")

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO configure_channel (log_id, channel_id, channel_name)
    VALUES (?, ?, ?)
    """, (log_id, channel.id, channel.name))
    connection.commit()
    connection.close()

    return log_id


def catch_peep(description: str, ctx: Context, peep_amount: int, random_integer: int) -> int:
    log_id = command("peep", description, ctx, "member")

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO catch_peep (log_id, peep_amount, random_integer)
    VALUES (?, ?, ?,)
    """, (log_id, peep_amount, random_integer))
    connection.commit()
    connection.close()

    return log_id


def psps_denied(ctx: Context, reason: str) -> int:
    log_id = command("peep", "psps denied", ctx, "member")

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO psps_denied (log_id, reason)
    VALUES (?, ?)
    """, (log_id, reason))
    connection.commit()
    connection.close()

    return log_id


def change_peep_message(interaction: Interaction, message_type: str, old_message: str, new_message: str) -> int:
    log_id = command("config", "PeepMessage changed", interaction, "manager")

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO change_peep_message (log_id, message_type, old_message, new_message)
    VALUES (?, ?, ?, ?)
    """, (log_id, message_type, old_message, new_message))
    connection.commit()
    connection.close()

    return log_id


def help_embed(help_type: str, context: Union[Context, Interaction], command_type: str) -> int:
    log_id = command("bot", "HelpEmbed sent", context, command_type)

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO help (log_id, type)
    VALUES (?, ?)
    """, (log_id, help_type))
    connection.commit()
    connection.close()

    return log_id
