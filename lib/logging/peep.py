import sqlite3
from typing import TYPE_CHECKING

from lib.logging.base import command
from lib.getter.config import log_path

if TYPE_CHECKING:
    from discord.ext.commands.context import Context


__all__ = [
    "catch_peep",
    "psps_denied",
    "steal_peep"
]



def catch_peep(description: str, ctx: "Context", peep_amount: int, random_integer: int) -> int:
    log_id = command("peep", description, ctx, "member")

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO catch_peep (log_id, peep_amount, random_integer)
    VALUES (?, ?, ?)
    """, (log_id, peep_amount, random_integer))
    connection.commit()
    connection.close()

    return log_id


def psps_denied(ctx: "Context", reason: str) -> int:
    log_id = command("peep", "psps denied", ctx, "member")

    connection = sqlite3.connect(log_path())
    connection.execute("""
    INSERT INTO psps_denied (log_id, reason)
    VALUES (?, ?)
    """, (log_id, reason))
    connection.commit()
    connection.close()

    return log_id


def steal_peep(context: "Context", mod: str, emote: str) -> int:
    log_id = command("peep", "Peep got stolen", context, "member")

    con = sqlite3.connect(log_path())
    con.execute("""
    INSERT INTO steal_peep (log_id, mod, emote)
    VALUES (?, ?, ?)
    """, (log_id, mod, emote))
    con.commit()
    con.close()

    return log_id
