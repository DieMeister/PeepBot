import sqlite3
from typing import TYPE_CHECKING, Optional

from lib.logging import command, Module, CommandType
from lib.getter.config import log_path

if TYPE_CHECKING:
    from discord import Interaction
    from discord.ext.commands.context import Context


__all__ = [
    "catch_peep",
    "psps_denied",
    "steal_peep",
    "peep_transfer",
    "rank",
    "give_peeps"
]



def catch_peep(description: str, ctx: "Context", peep_amount: int, random_integer: int) -> int:
    log_id = command(Module.PEEP, description, ctx, CommandType.MEMBER)

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO catch_peep (log_id, peep_amount, random_integer)
    VALUES (?, ?, ?)
    """, (log_id, peep_amount, random_integer))
    connection.commit()
    connection.close()

    return log_id


def psps_denied(ctx: "Context", reason: str) -> int:
    log_id = command(Module.PEEP, "psps denied", ctx, CommandType.MEMBER)

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO psps_denied (log_id, reason)
    VALUES (?, ?)
    """, (log_id, reason))
    connection.commit()
    connection.close()

    return log_id


def steal_peep(context: "Context", mod: str, emote: str) -> int:
    log_id = command(Module.PEEP, "Peep got stolen", context, CommandType.MEMBER)

    con = sqlite3.connect(log_path())
    con.execute("""
    INSERT INTO steal_peep (log_id, moderator, emote)
    VALUES (?, ?, ?)
    """, (log_id, mod, emote))
    con.commit()
    con.close()

    return log_id


def peep_transfer(description: str, interaction: "Interaction", amount: int, recipient_id: int, sender_peeps: Optional[int]=None, receiver_peeps: Optional[int]=None) -> int:
    log_id = command(Module.PEEP, description, interaction, CommandType.MEMBER)

    con = sqlite3.connect(log_path())
    con.execute("""
    INSERT INTO peep_transfer (log_id, peep_amount, recipient_id, sender_peeps, receiver_peeps)
    VALUES (?, ?, ?, ?, ?)
    """, (log_id, amount, recipient_id, sender_peeps, receiver_peeps))
    con.commit()
    con.close()

    return log_id


def rank(interaction: "Interaction", user_id: int) -> int:
    log_id = command(Module.PEEP, "RankCommand sent", interaction, CommandType.MEMBER)

    log_db = sqlite3.connect(log_path())
    log_db.execute("""
    INSERT INTO rank_command (log_id, rank_user_id)
    VALUES (?, ?)
    """, (log_id, user_id))
    log_db.commit()
    log_db.close()

    return log_id


def give_peeps(given_peeps: int, guild_id: int, user_id: int, context: "Context", ) -> int:
    """Log when peeps are given to a member.

    Return the log_id.

    Parameters
    -----------
    given_peeps: :class:`int`
        The amount of peeps the member should get.
    guild_id: :class:`int`
        The id of the member's guild.
    user_id: :class:`int`
        The user_id of the member.
    context: :class:`Context`
        The context of the command.
    """
    log_id = command(Module.PEEP, "peeps given to a member", context, CommandType.DEVELOPER)

    log_db = sqlite3.connect(log_path())
    log_db.execute("""
    INSERT INTO give_peeps (
        log_id,
        amount,
        member_guild_id,
        member_user_id
    )
    VALUES (?, ?, ?, ?)
    """, (log_id, given_peeps, guild_id, user_id))
    log_db.commit()
    log_db.close()

    return log_id