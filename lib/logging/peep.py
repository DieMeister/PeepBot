import sqlite3
from typing import TYPE_CHECKING, Optional

from lib.logging import command
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
    "give_peeps",
    "remove_peeps"
]



def catch_peep(description: str, ctx: "Context", peep_amount: int, random_integer: int) -> int:
    """Log when a member tries to get a peep.

    This function is only invoked when the member has the right to catch a peep at the moment.
    This function is invoked regardless of the outcome of the try.
    Return the log_id.

    Parameters
    -----------
    description: :class:`str`
        Short description of what happened.
    ctx: :class:`Context`
        The context of the psps command.
    peep_amount: :class:`int`
        The number of peeps the member has after executing the command.
    random_integer: :class:`int`
        The randomly selected integer that decided if the member got a peep.
    """
    log_id = command("peep", description, ctx, "member")

    log_db = sqlite3.connect(log_path())
    log_db.execute("""
    INSERT INTO catch_peep (log_id, peep_amount, random_integer)
    VALUES (?, ?, ?)
    """, (log_id, peep_amount, random_integer))
    log_db.commit()
    log_db.close()

    return log_id


def psps_denied(ctx: "Context", reason: str) -> int:
    """Log when member tries to get a peep without permission.

    Return the log_id.

    Parameters
    -----------
    ctx: :class:`Context`
        The context of the psps command.
    reason: :class:`str`
        The reason why the member does not have permission to execute the command.
    """
    log_id = command("peep", "psps denied", ctx, "member")

    log_db = sqlite3.connect(log_path())
    log_db.execute("""
    INSERT INTO psps_denied (log_id, reason)
    VALUES (?, ?)
    """, (log_id, reason))
    log_db.commit()
    log_db.close()

    return log_id


def steal_peep(context: "Context", mod: str, emote: str) -> int:
    """Log when a peep gets stolen.

    Return log_id.

    Parameters
    -----------
    context: :class:`Context`
        The context of the command.
    mod: :class:`str`
        The moderator that stole the peep.
    emote: :class:`str`
        The emote of the moderator.
    """
    log_id = command("peep", "Peep got stolen", context, "member")

    log_db = sqlite3.connect(log_path())
    log_db.execute("""
    INSERT INTO steal_peep (log_id, moderator, emote)
    VALUES (?, ?, ?)
    """, (log_id, mod, emote))
    log_db.commit()
    log_db.close()

    return log_id


def peep_transfer(description: str, interaction: "Interaction", amount: int, recipient_id: int, sender_peeps: Optional[int]=None, receiver_peeps: Optional[int]=None) -> int:
    """Log the transfer of peeps and its attempts.

    Return log_id.

    Parameters
    -----------
    description: :class:`str`
        A short description of what happened.
    interaction: :class:`Interaction`
        The interaction of the command.
    amount: :class:`int`
        The amount of peeps that a member wants to transfer.
    recipient_id: :class:`int`
        The discord id of the member who receives the peeps if the transfer is successful.
    sender_peeps: :class:`int`
        The amount of peeps the member who transfers their peeps had before executing the command.
    receiver_peeps: :class:`int`
        The amount of peeps the member who gets the peeps had before the execution of the command.
    """
    log_id = command("peep", description, interaction, "member")

    log_db = sqlite3.connect(log_path())
    log_db.execute("""
    INSERT INTO peep_transfer (log_id, peep_amount, recipient_id, sender_peeps, receiver_peeps)
    VALUES (?, ?, ?, ?, ?)
    """, (log_id, amount, recipient_id, sender_peeps, receiver_peeps))
    log_db.commit()
    log_db.close()

    return log_id


def rank(interaction: "Interaction", user_id: int) -> int:
    """Log the execution of /rank

    Return the log_id.

    Parameters
    -----------
    interaction: :class:`Interaction`
        The interaction of the command.
    user_id: :class:`int`
        The discord id of the member whose rank was requested.
    """
    log_id = command("peep", "RankCommand sent", interaction, "member")

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
    log_id = command("peep", "peeps given to a member", context, "developer")

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


def remove_peeps(old_total: int, amount_removed: int, guild_id: int, user_id: int, context: "Context") -> int:
    """
    Log when peeps are removed from a member.

    If `amount_removed` > `old_total` the new total is 0, not a negative number.
    Return the log id.

    Parameters
    -----------
    old_total: :class:`int`
        The amount of peeps the member had before.
    amount_removed: :class:`int`
        The amount of peeps the member now has less than before.
    guild_id: :class:`int`
        The member's guild_id.
    user_id: :class:`int`
        The member's user_id.
    context: :class:`Context`
        The context of the command.
    """
    log_id = command("peep", "peeps removed from member", context, "developer")

    log_db = sqlite3.connect(log_path())
    log_db.execute("""
    INSERT INTO remove_peeps (
        log_id,
        old_total,
        amount_removed,
        member_guild_id,
        member_user_id
    )
    VALUES (?, ?, ?, ?, ?)
    """, (log_id, old_total, amount_removed, guild_id, user_id))
    log_db.commit()
    log_db.close()

    return log_id
