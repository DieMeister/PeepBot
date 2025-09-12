from discord import Embed
from typing import TYPE_CHECKING

import datetime as dt
from datetime import datetime

from lib import config
from lib.getter.date_time import discord_dt_string

if TYPE_CHECKING:
    from lib import types
    from discord import Member, Guild


__all__ = [
    "rank",
    "leaderboard"
]


def rank(member: "Member", tries: str, total: str, gifted: str, received: str) -> Embed:
    """
    Return the discord embed to send after executing /rank

    Parameters
    -----------
    member: :class:`Member`
        The discord member the stats are about.
    tries: :class:`str`
        The amount the member tried to get a peep.
    total: :class:`str`
        The peeps the member has in total.
    gifted: :class:`str`
        The amount of peeps the member gifted to other members.
    received: :class:`str`
        The amount of peeps the member got gifted from other members or  given by a developer
    """
    author: "types.Author" = {
        "name": member.display_name,
        "icon_url": member.avatar.url,
        "url": None
    }
    embed: "types.Embed" = {
        "type": "rich",
        "title": "Rank",
        "description": f"{config.emote('tries')} {tries}\n{config.emote('peeps')} {total}\n{config.emote('gifted')} {gifted}\n{config.emote('received')} {received}",
        "url": None,
        "timestamp": discord_dt_string(datetime.now(dt.UTC)),
        "color": config.embed_color(),
        "footer": None,
        "image": None,
        "thumbnail": None,
        "author": author,
        "fields": None
    }
    return Embed.from_dict(embed)


def leaderboard(guild: "Guild", leaders: list[tuple[int, int, int, int, int]]) -> Embed:
    """
    Return a discord embed of the ten members of a guild with the most peeps.

    Parameters
    -----------
    guild: :class:`Guild`
        The guild the leaderboard belongs to.
    leaders: :class:`list[:class:`tuple[:class:`int`, :class:`int`, :class:`int`, :class:`int`, :class:`int`]`]`
        The list of the ten members.
        The length of the list is always between 0 and 10.
        Each entry is a tuple of the user_id, total peeps, tries, sent peeps, and received peeps.
    """
    fields: list["types.Field"] = []
    for leader in leaders:
        user_id, total, tries, sent, received = leader
        member = guild.get_member(user_id)
        field: "types.Field" = {
            "name": member.display_name,
            "value": f"{config.emote('tries')} {tries} | {config.emote('peeps')} {total} | {config.emote('gifted')} {sent} | {config.emote('received')} {received}",
            "inline": False
        }
        fields.append(field)
    embed: "types.Embed" = {
        "title": "Leaderboard",
        "type": "rich",
        "description": None,
        "url": None,
        "timestamp": discord_dt_string(datetime.now(dt.UTC)),
        "color": config.embed_color(),
        "footer": None,
        "image": None,
        "thumbnail": None,
        "author": None,
        "fields": fields
    }
    return Embed.from_dict(embed)
