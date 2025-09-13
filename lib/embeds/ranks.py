import datetime as dt
from datetime import datetime

import discord
from typing import TYPE_CHECKING
from lib import config, utils

if TYPE_CHECKING:
    from discord import Member, Guild
    from discord.types.embed import EmbedAuthor, Embed, EmbedField


__all__ = [
    "rank",
    "leaderboard"
]


def rank(member: "Member", tries: str, total: str, gifted: str, received: str) -> discord.Embed:
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
    author: "EmbedAuthor" = {
        "name": member.display_name,
        "icon_url": member.avatar.url
    }
    embed: "Embed" = {
        "type": "rich",
        "title": "Rank",
        "description": f"{config.emote('tries')} {tries}\n{config.emote('peeps')} {total}\n{config.emote('gifted')} {gifted}\n{config.emote('received')} {received}",
        "timestamp": utils.discord_dt_string(datetime.now(dt.UTC)),
        "color": config.embed_color(),
        "author": author
    }
    return discord.Embed.from_dict(embed)


def leaderboard(guild: "Guild", leaders: list[tuple[int, int, int, int, int]]) -> discord.Embed:
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
    fields: list["EmbedField"] = []
    for leader in leaders:
        user_id, total, tries, sent, received = leader
        member = guild.get_member(user_id)
        field: "EmbedField" = {
            "name": member.display_name,
            "value": f"{config.emote('tries')} {tries} | {config.emote('peeps')} {total} | {config.emote('gifted')} {sent} | {config.emote('received')} {received}",
            "inline": False
        }
        fields.append(field)
    embed: "Embed" = {
        "title": "Leaderboard",
        "type": "rich",
        "timestamp": utils.discord_dt_string(datetime.now(dt.UTC)),
        "color": config.embed_color(),
        "fields": fields
    }
    return discord.Embed.from_dict(embed)
