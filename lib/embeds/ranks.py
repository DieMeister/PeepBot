from discord import Embed
from typing import TYPE_CHECKING

import datetime as dt
from datetime import datetime

from lib.getter.config import tries_emote, peeps_emote, gifted_emote, received_emote
from lib.getter.config import embed_color
from lib.getter.date_time import discord_dt_string

if TYPE_CHECKING:
    from lib import types
    from discord import Member, Guild


__all__ = [
    "rank",
    "leaderboard"
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


def leaderboard(guild: "Guild", leaders: list[tuple[int, int, int, int, int]]) -> Embed:
    fields: list["types.Field"] = []
    for leader in leaders:
        user_id, total, tries, sent, received = leader
        member = guild.get_member(user_id)
        field: "types.Field" = {
            "name": member.display_name,
            "value": f"{tries_emote()} {tries} | {peeps_emote()} {total} | {gifted_emote()} {sent} | {received_emote()} {received}",
            "inline": False
        }
        fields.append(field)
    embed: "types.Embed" = {
        "title": "Leaderboard",
        "type": "rich",
        "description": None,
        "url": None,
        "timestamp": discord_dt_string(datetime.now(dt.UTC)),
        "color": embed_color(),
        "footer": None,
        "image": None,
        "thumbnail": None,
        "author": None,
        "fields": fields
    }
    return Embed.from_dict(embed)
