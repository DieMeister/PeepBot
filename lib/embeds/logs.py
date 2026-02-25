from discord import Embed
from typing import Optional, TYPE_CHECKING

import datetime as dt
from datetime import datetime

from lib.getter.config import embed_color
from lib.getter.date_time import discord_dt_string

if TYPE_CHECKING:
    from lib import types


__all__ = [
    "role_log",
    "channel_log"
]


def _default_log(log_id: str, action: str, fields: Optional[list["types.Field"]]) -> Embed:
    """
    A blueprint for discord embed logs.

    Parameters
    -----------
    log_id: :class:`str`
        The id the event is saved in the log database of the bot.
    action: :class:`str`
        A short description of what happened.
    fields: Optional[:class:`list[:class:`dict`]`
        The fields to add to the embed.
        Can be a maximum of 25 fields.
    """
    footer: "types.Footer" = {
            "text": f"LogId: {log_id}",
            "icon_url": None
        }
    embed: "types.Embed" = {
        "type": "rich",
        "title": action,
        "description": None,
        "color": embed_color(),
        "timestamp": discord_dt_string(datetime.now(dt.UTC)),
        "footer": footer,
        "fields": fields,
        "url": None,
        "image": None,
        "thumbnail": None,
        "author": None
    }
    return Embed.from_dict(embed)


def role_log(log_id: str, action: str, role_id: str, moderator_id: str, reason: Optional[str], receiver_id: Optional[str]=None) -> Embed:
    """
    Return a discord embed that acts as log for actions about AssignableRoles.

    Parameters
    -----------
    log_id: :class:`str`
        The log_id used in the bot's log database.
    action: :class:`str`
        A short description of the actions.
    role_id: :class:`str`
        The discord id of the role.
    moderator_id: :class:`str`
        the discord id of the moderator responsible for the action.
    reason: Optional8:class:`str`]
        The reason why the moderator executed the action.
    receiver_id: Optional[:class:`str`]=None
        The discord id of the receiver if a receiver exists.
    """
    fields: list["types.Field"] = [
        {
            "name": "Role",
            "value": f"<@&{role_id}>",
            "inline": True
        },
        {
            "name": "Moderator",
            "value": f"<@{moderator_id}>",
            "inline": True
        }
    ]
    if receiver_id is not None:
        fields.append({
            "name": "Receiver",
            "value": f"<@{receiver_id}>",
            "inline": True
        })
    if reason is not None:
        fields.append({
            "name": "Reason",
            "value": reason,
            "inline": True
        })
    return _default_log(log_id, action, fields)


def channel_log(log_id: str, action: str, channel_id: str, moderator_id: str) -> Embed:
    fields: list["types.Field"] = [
        {
            "name": "Channel",
            "value": f"<#{channel_id}>",
            "inline": True
        },
        {
            "name": "Moderator",
            "value": f"<@{moderator_id}>",
            "inline": True
        }
    ]
    return _default_log(log_id, action, fields)
