import datetime as dt
from datetime import datetime

import discord
from typing import TYPE_CHECKING
from lib import config, utils

if TYPE_CHECKING:
    from discord.types.embed import Embed, EmbedField, EmbedFooter


__all__ = [
    "dev"
]


def dev() -> discord.Embed:
    """Return a discord embed that contains information for developers."""
    divider_commands: "EmbedField" = {
        "name": "Commands",
        "value": "\u200b",
        "inline": False
    }
    command_reload_cog: "EmbedField" = {
        "name": "reload_cog <Cog>",
        "value": "Reloads a provided Cog",
        "inline": True
            }
    command_unload_cog: "EmbedField" = {
        "name": "unload_cog <Cog>",
        "value": "Unloads a before loaded Cog.\n**WARNING:** once the Cog `Bot` is unloaded it can not be loaded again, use `reload_cog` if something doesn't work instead.",
        "inline": True
    }
    command_load_cog: "EmbedField" = {
        "name": "load_cog <Cog>",
        "value": "Loads a before unloaded Cog.",
        "inline": True
    }
    command_sync: "EmbedField" = {
        "name": "sync",
        "value": "Syncs every ApplicationCommand with Discord. Needs to be done whenever an ApplicationCommand is changed in the Bot's source code",
        "inline": True
    }
    command_shutdown: "EmbedField" = {
        "name": "shutdown",
        "value": "Shuts down the Bot causing it to stop running. This should only be done when absolutely necessary since it cannot be undone from within Discord",
        "inline": True
    }
    command_help: "EmbedField" = {
        "name": "help",
        "value": "Shows this message.\nIf this leaves unanswered questions feel free to dm `@diemeister`",
        "inline": True
    }
    command_give_peep: "EmbedField" = {
        "name": "give_peeps <amount> <user_id> <guild_id>",
        "value": "Gives a set amount of peeps to a member.\n`amount`: The amount of peeps the member gets. Must be at least 1.\n`user_id`: The user_id of the member.\n`guild_id`: The id of the member's guild.",
        "inline": True
    }
    command_remove_peeps: "EmbedField" = {
        "name": "remove_peeps <amount> <user_id> <guild_id>",
        "value": "Removes a provided amount of peeps from a provided member.\nThe command need not be executed in the member's guild.\n`amount`: The number of peeps that is taken away from the member.\nMust be at least 1\nIf the member has less peeps than this number their total peeps is set to 0.\n`user_id`: The member's user_id.\n`guild_id`:The member's guild_id.",
        "inline": False
    }
    cog_divider: "EmbedField" = {
        "name": "List of Cogs and a description",
        "value": "\u200b",
        "inline": False
    }
    cog_bot: "EmbedField" = {
        "name": "Bot",
        "value": "Core functionality of the Bot, this includes loading and unloading Cogs, as well as automatically making Database backups.",
        "inline": True
    }
    cog_config: "EmbedField" = {
        "name": "Config",
        "value": "Configure the Bot for each Guild, this includes changing the PeepMessage, adding and removing PspsChannels, adding and removing AssignableRoles to the List of AssignableRoles, and setting a LogChannel",
        "inline": True
    }
    cog_easter_egg: "EmbedField" = {
        "name": "EasterEgg",
        "value": "Includes all 'hidden' commands",
        "inline": True
    }
    cog_help: "EmbedField" = {
        "name": "Help",
        "value": "Responsible for sending HelpMessages (both `devhelp` and `help`)",
        "inline": True
    }
    cog_moderation: "EmbedField" = {
        "name": "Moderation",
        "value": "This contains functionality about AssignableRoles, such as commands to remove a role from and add a role to a member",
        "inline": True
    }
    cog_peep: "EmbedField" = {
        "name": "Peep",
        "value": "Includes everything directly connected to Peeps, such as psps, rank, and leaderboard commands",
        "inline": True
    }
    divider_info: "EmbedField" = {
        "name": "Other Information",
        "value": "\u200b",
        "inline": False
    }
    prefixes: "EmbedField" = {
        "name": "Prefixes",
        "value": "The bot supports `!pb!`, `!`, and `?` as prefixes.\nThis is only important for the commands listed above.",
        "inline": True
    }
    info_loop: "EmbedField" = {
        "name": "Loops",
        "value": f"Everyday at {discord.utils.format_dt(datetime(2007, 6, 6, 1, 0, tzinfo=dt.UTC), style='t')} (01:00 UTC)",
        "inline": True
    }
    footer: "EmbedFooter" = {
        "text": "Help"
    }

    embed: "Embed" = {
        "type": "rich",
        "title": "Developer Help",
        "description": "Explains every DeveloperCommand",
        "color": config.embed_color(),
        "timestamp": utils.dt_string(datetime(2025, 9, 8, 10, 45, tzinfo=dt.UTC)),
        "footer": footer,
        "fields": [
            divider_commands,
            command_reload_cog,
            command_unload_cog,
            command_load_cog,
            command_sync,
            command_shutdown,
            command_help,
            command_give_peep,
            command_remove_peeps,
            cog_divider,
            cog_bot,
            cog_config,
            cog_easter_egg,
            cog_help,
            cog_moderation,
            cog_peep,
            divider_info,
            prefixes,
            info_loop
        ]
    }
    return discord.Embed.from_dict(embed)
