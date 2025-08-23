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


def default_log(log_id: str, action: str, fields: Optional[list["types.Field"]]) -> Embed:
    embed: "types.Embed" = {
        "type": "rich",
        "title": action,
        "description": None,
        "color": embed_color(),
        "timestamp": discord_dt_string(datetime.now(dt.UTC)),
        "footer": {
            "text": f"LogId: {log_id}",
        },
        "fields": fields
    }
    return Embed.from_dict(embed)


def role_log(log_id: str, action: str, role_id: str, moderator_id: str, reason: Optional[str], receiver_id: Optional[str]=None) -> Embed:
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
    return default_log(log_id, action, fields)


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
    return default_log(log_id, action, fields)
