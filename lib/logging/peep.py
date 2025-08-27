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
    "peep_transfer"
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
    INSERT INTO steal_peep (log_id, mod, emote)
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
