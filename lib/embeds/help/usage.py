import datetime as dt
from datetime import datetime

from typing import TYPE_CHECKING
from discord import Embed

from lib import config
from lib.getter import discord_dt_string

if TYPE_CHECKING:
    from lib import types


__all__ = [
    "use_peep",
    "use_assignable_roles"
]


def use_peep() -> Embed:
    """Return a discord embed that contains information about how to use the peep part of the bot."""
    psps: "types.Field" = {
        "name": "!psps",
        "value": "- Use this command to get peeps. This only works in a before defined channel (`/add_psps_channel`)\n- You have to wait 10 minutes before you can use the command again\n- You have to wait 1 minute after someone else used to command\n- The probability to catch a peep is 1/7",
        "inline": True
    }
    rank: "types.Field" = {
        "name": "/rank",
        "value": "Shows how many Peeps and how often you tried to get the Peeps",
        "inline": True
    }
    leaderboard: "types.Field" = {
        "name": "/leaderboard",
        "value": "Shows the 10 members with the most Peeps. If two members have the same amount, the lower user_id is picked first",
        "inline": True
    }
    transfer_peeps: "types.Field" = {
        "name": "/transfer_peeps <amount> <recipient>",
        "value": "Transfers some or all of your peeps to another member\n`amount`: The number of peeps you want to transfer\n`recipient`: The member who gets your peeps",
        "inline": True
    }
    footer: "types.Footer" = {
            "text": "Help",
            "icon_url": None
        }
    embed: "types.Embed" = {
        "type": "rich",
        "title": "Peep Usage",
        "description": "How to use everything concerning Peeps",
        "color": config.embed_color(),
        "timestamp": discord_dt_string(datetime(2025, 8, 23, 0, 50, tzinfo=dt.UTC)),
        "footer": footer,
        "fields": [
            psps,
            rank,
            leaderboard,
            transfer_peeps
        ],
        "url": None,
        "image": None,
        "thumbnail": None,
        "author": None
    }
    return Embed.from_dict(embed)


def use_assignable_roles() -> Embed:
    """Return a discord embed that contains information about how to use the assignable role part of the bot."""
    add_role: "types.Field" = {
        "name": "/add_role <role_id> <member> [reason]",
        "value": "Gives a member a role from a predefined list\n`role_id`: The role that is given to the member\n`member`: The member that gets the role\n`reason`: Optional - The reason why the member gets the role",
        "inline": True
    }
    remove_role: "types.Field" = {
        "name": "/remove_role <role_id> <member> [reason]",
        "value": "Removes a role from a predefined list from a member\n`role_id`: The role that is removed from the member\n`member`: The member that looses the role\n`reason`: Optional - The reason why the member looses the role",
        "inline": True
    }
    footer: "types.Footer" = {
            "text": "Help",
            "icon_url": None
        }
    embed: "types.Embed" = {
        "type": "rich",
        "title": "AssignableRoles Usage",
        "description": "How to use everything concerning AssignableRoles",
        "color": config.embed_color(),
        "timestamp": discord_dt_string(datetime(2025, 8, 23, 0, 50, tzinfo=dt.UTC)),
        "footer": footer,
        "fields": [
            add_role,
            remove_role
        ],
        "url": None,
        "image": None,
        "thumbnail": None,
        "author": None
    }
    return Embed.from_dict(embed)
