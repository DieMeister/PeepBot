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
    """
    Return the discord embed to send after executing /rank

    Parameters
    -----------
    member: :class:`Member`
        The discord member the stats are about.
    tries: :class:`str`
        The amount the member tried to get a peep.
    total: :class:`str`
        The peeps a the member has in total.
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
