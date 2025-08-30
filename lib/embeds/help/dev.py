import discord
from discord import Embed

import datetime as dt
from datetime import datetime

from typing import TYPE_CHECKING

from lib.getter import embed_color, dt_string

if TYPE_CHECKING:
    from lib import types


__all__ = [
    "dev"
]


def dev() -> "Embed":
    divider_commands: "types.Field" = {
        "name": "Commands",
        "value": "\u200b",
        "inline": False
    }
    command_reload_cog: "types.Field" = {
        "name": "reload_cog <Cog>",
        "value": "Reloads a provided Cog",
        "inline": True
            }
    command_unload_cog: "types.Field" = {
        "name": "unload_cog <Cog>",
        "value": "Unloads a before loaded Cog.\n**WARNING:** once the Cog `Bot` is unloaded it can not be loaded again, use `reload_cog` if something doesn't work instead.",
        "inline": True
    }
    command_load_cog: "types.Field" = {
        "name": "load_cog <Cog>",
        "value": "Loads a before unloaded Cog.",
        "inline": True
    }
    command_sync: "types.Field" = {
        "name": "sync",
        "value": "Syncs every ApplicationCommand with Discord. Needs to be done whenever an ApplicationCommand is changed in the Bot's source code",
        "inline": True
    }
    command_shutdown: "types.Field" = {
        "name": "shutdown",
        "value": "Shuts down the Bot causing it to stop running. This should only be done when absolutely necessary since it cannot be undone from within Discord",
        "inline": True
    }
    command_help: "types.Field" = {
        "name": "help",
        "value": "Shows this message.\nIf this leaves unanswered questions feel free to dm `@diemeister`",
        "inline": True
    }
    cog_divider: "types.Field" = {
        "name": "List of Cogs and a description",
        "value": "\u200b",
        "inline": False
    }
    cog_bot: "types.Field" = {
        "name": "Bot",
        "value": "Core functionality of the Bot, this includes loading and unloading Cogs, as well as automatically making Database backups.",
        "inline": True
    }
    cog_config: "types.Field" = {
        "name": "Config",
        "value": "Configure the Bot for each Guild, this includes changing the PeepMessage, adding and removing PspsChannels, adding and removing AssignableRoles to the List of AssignableRoles, and setting a LogChannel",
        "inline": True
    }
    cog_easter_egg: "types.Field" = {
        "name": "EasterEgg",
        "value": "Includes all 'hidden' commands",
        "inline": True
    }
    cog_help: "types.Field" = {
        "name": "Help",
        "value": "Responsible for sending HelpMessages (both `devhelp` and `help`)",
        "inline": True
    }
    cog_moderation: "types.Field" = {
        "name": "Moderation",
        "value": "This contains functionality about AssignableRoles, such as commands to remove a role from and add a role to a member",
        "inline": True
    }
    cog_peep: "types.Field" = {
        "name": "Peep",
        "value": "Includes everything directly connected to Peeps, such as psps, rank, and leaderboard commands",
        "inline": True
    }
    divider_info: "types.Field" = {
        "name": "Other Information",
        "value": "\u200b",
        "inline": False
    }
    info_loop: "types.Field" = {
        "name": "Loops",
        "value": f"Everyday at {discord.utils.format_dt(datetime(2007, 6, 6, 1, 0, tzinfo=dt.UTC), style="t")} (01:00 UTC)",
        "inline": True
    }

    embed: "types.Embed" = {
        "type": "rich",
        "title": "Developer Help",
        "description": "Explains every DeveloperCommand",
        "color": embed_color(),
        "timestamp": dt_string(datetime(2025, 8, 22, 22, 50, tzinfo=dt.UTC)),
        "footer": {
            "text": "Help"
        },
        "fields": [
            divider_commands,
            command_reload_cog,
            command_unload_cog,
            command_load_cog,
            command_sync,
            command_shutdown,
            command_help,
            cog_divider,
            cog_bot,
            cog_config,
            cog_easter_egg,
            cog_help,
            cog_moderation,
            cog_peep,
            divider_info,
            info_loop
        ],
        "url": None,
        "image": None,
        "thumbnail": None,
        "author": None
    }
    return Embed.from_dict(embed)