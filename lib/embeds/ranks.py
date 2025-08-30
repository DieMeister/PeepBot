from discord import Embed
from typing import TYPE_CHECKING

import datetime as dt
from datetime import datetime

from lib.getter.config import tries_emote, peeps_emote, gifted_emote, received_emote
from lib.getter.config import embed_color
from lib.getter.date_time import discord_dt_string

if TYPE_CHECKING:
    from lib import types
    from discord import Member


__all__ = [
    "rank"
]


def rank(member: "Member", tries: str, total: str, gifted: str, received: str) -> Embed:
    author: "types.Author" = {
        "name": member.display_name,
        "icon_url": member.avatar.url,
        "url": None
    }
    embed: "types.Embed" = {
        "type": "rich",
        "title": "Rank",
        "description": f"{tries_emote()} {tries}\n{peeps_emote()} {total}\n{gifted_emote()} {gifted}\n{received_emote()} {received}",
        "url": None,
        "timestamp": discord_dt_string(datetime.now(dt.UTC)),
        "color": embed_color(),
        "footer": None,
        "image": None,
        "thumbnail": None,
        "author": author,
        "fields": None
    }
    return Embed.from_dict(embed)
