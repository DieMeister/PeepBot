import datetime as dt
from datetime import datetime

from typing import TYPE_CHECKING
import discord

from lib.getter import dt_string
from lib.getter.config import embed_color

if TYPE_CHECKING:
    from discord import Embed
    from lib import types

__all__ = [
    "devhelp",
    "help_config",
    "help_usage"
]


def devhelp() -> "Embed":
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
        "value": f"Everyday at {discord.utils.format_dt(datetime(0, 0, 0, 1, tzinfo=dt.UTC))} (01:00 UTC)",
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
        ]
    }
    return Embed.from_dict(embed)


def help_config() -> "Embed":
    divider_psps: "types.Field" = {
        "name": "Peep",
        "value": "\u200b",
        "inline": False
    }
    psps_add_psps_channel: "types.Field" = {
        "name": "add_psps_channel <channel>",
        "value": "Adds a channel where the psps command can be executed. By default the command works in no channel\n`channel`: The channel that is being added",
        "inline": True
    }
    psps_remove_psps_channel: "types.Field" = {
        "name": "remove_psps_channel <channel>",
        "value": "Removes a channel from the list of channels where the pssp command works\n`channel`: The channel that is being removed",
        "inline": True
    }
    psps_change_psps_message: "types.Field" = {
        "name": "change_psps_message <message_type> <message>",
        "value": "changes the message that is sent when psps is executed\n`message_type`: The Message that is being changed (`No Peep`, `Peep scratched you`, or `You got a peep`\n`message`: The content the Message is being changed to",
        "inline": True
    }
    divider_assignable_role: "types.Field" = {
        "name": "Assignable Role",
        "value": "!!The Bot's highest Role must be higher than the Members highest Role in order to add or remove Roles to said Member!!",
        "inline": False
    }
    ar_add_assignable_role: types.Field = {
        "name": "add_assignable_role <role> [reason]",
        "value": "Adds a Role to the list of Roles that can be assigned to Members using `/add_role`\n`role`: The Role that is being added\n`reason`: Optional - The reason why the Role is being added",
        "inline": True
    }
    ar_remove_assignable_role: types.Field = {
        "name": "remove_assignable_role <role> [reason]",
        "value": "Removes a Roles from the list of Roles that can be assigned to members using `/add_role`\n`role`: The Role that is being removed\n`reason`: Optional - the reason why the Role is being removed",
        "inline": True
    }
    set_log_channel: types.Field = {
        "name": "set_log_channel <channel>",
        "value": "Sets the provided TextChannel as the Channel where the Bot sends LogMessages\n`channel`: The Channel that is set as new LogChannel",
        "inline": False
    }

    embed: "types.Embed" = {
        "type": "rich",
        "title": "Configuration Help",
        "description": "Everything you need to do to make the Bot work",
        "color": embed_color(),
        "timestamp": dt_string(datetime(2025, 8, 22, 23, 37, tzinfo=dt.UTC)),
        "footer": {
            "text": "Help"
        },
        "fields": [
            divider_psps,
            psps_add_psps_channel,
            psps_remove_psps_channel,
            psps_change_psps_message,
            divider_assignable_role,
            ar_add_assignable_role,
            ar_remove_assignable_role,
            set_log_channel
        ]
    }
    return Embed.from_dict(embed)


def help_usage() -> "Embed":
    divider_psps: "types.Field" = {
        "name": "Psps",
        "value": "\u200b",
        "inline": False
    }
    psps_psps: "types.Field" = {
        "name": "psps",
        "value": "- To get peeps type `!psps` in an allowed chat, if you don't know which chats are allowed ask your server manager, admin, or owner. If you are the person responsible to set up the bot please execute /help <setup>\n- You have to wait 10 minutes before you can execute the command again.\n- You have to wait 1 minute after someone else executed the command before you can execute it.\n- The probability to catch a peep is 1/7.",
        "inline": True
    }
    psps_rank: "types.Field" = {
        "name": "/leaderboard",
        "value": "Shows the 10 Members of the server with the most Peeps. If two Members have the same amount the lower user_id is picked first",
        "inline": True
    }
    psps_leaderboard: "types.Field" = {
        "name": "/rank",
        "value": "Shows your current amount of Peeps and the Tries it took you",
        "inline": True
    }
    divider_role: "types.Field" = {
        "name": "Assign Roles",
        "value": "\u200b",
        "inline": False
    }
    role_add_role: "types.Field" = {
        "name": "/add_role <role_id> <member> [reason]",
        "value": "Adds a Role from a predefined list to a Member\n`role_id`: The Role that is assigned to the Member\n`member`: The Member that gets the Role\n`reason`: Optional - The Reason why the Role is given to the Member",
        "inline": True
    }
    role_remove_role: "types.Field" = {
        "name": "/remove_role <role_id> <member> [reason]",
        "value": "Removaes a Role from a predefined list from a Member\n`role_id`: The Role that is removed from the Member\n`member`: The Member that looses the Role\n`reason`: Optional - The Reason why the Role is being removed from the Member",
        "inline": True
    }


    embed: "types.Embed" = {
        "type": "rich",
        "title": "Usage help",
        "description": "Everything you need to know to use the Bot",
        "color": embed_color(),
        "timestamp": dt_string(datetime(2025, 8, 23, 0, 50, tzinfo=dt.UTC)),
        "footer": {
            "text": "Help"
        },
        "fields": [
            divider_psps,
            psps_psps,
            psps_rank,
            psps_leaderboard,
            divider_role,
            role_add_role,
            role_remove_role
        ]
    }
    return Embed.from_dict(embed)
