import datetime as dt
from datetime import datetime

from typing import TYPE_CHECKING
from discord import Embed

from lib.getter import embed_color, discord_dt_string

if TYPE_CHECKING:
    from lib import types


__all__ = [
    "config_peep",
    "config_assignable_role"
]


def config_peep() -> Embed:
    add_psps_channel: "types.Field" = {
        "name": "/add_psps_channel <channel>",
        "value": "Adds a channel where `!psps` can be executed\n`channel`: The channel that is being added",
        "inline": True
    }
    remove_psps_channel: "types.Field" = {
        "name": "/remove_psps_channel <channel>",
        "value": "Removes a channel where `!psps` can be executed.\n`channel`: The channel !psps can no longer be executed in",
        "inline": True
    }
    change_psps_message: "types.Field" = {
        "name": "/change_psps_message <message_type> <message>",
        "value": "Changes the message that is sent after `!psps` is executed\n`message_type`: The message which's content is being changed\n`message`: The new content of the message",
        "inline": True
    }

    embed: "types.Embed" = {
        "type": "rich",
        "title": "Config Peep",
        "description": "How to configure everything concerning Peeps",
        "color": embed_color(),
        "timestamp": discord_dt_string(datetime(2025, 8, 22, 23, 37, tzinfo=dt.UTC)),
        "footer": {
            "text": "Help"
        },
        "fields": [
            add_psps_channel,
            remove_psps_channel,
            change_psps_message
        ]
    }
    return Embed.from_dict(embed)


def config_assignable_role() -> Embed:
    add_assignable_role: "types.Field" = {
        "name": "/add_assignable_role <role> [reason]",
        "value": "Adds a role to the list of roles that can be assigned using `/add_role`\n`role`: the role that is being added\n`reason`: Optional - The reason why the role is being added",
        "inline": True
    }
    remove_assignable_role: "types.Field" = {
        "name": "/remove_assignable_role <role> [reason]",
        "value": "Removes a role from the list of roles that can be assigned using `/add_role`\n`role`: The role that is being removed\n`reason`: Optional - The reason why the role is being removed",
        "inline": True
    }
    set_log_channel: "types.Field" = {
        "name": "/set_log_channel <channel>",
        "value": "Sets the provided channel as the channel where the bot sends logs\n`channel`: The channel logs are being sent to",
        "inline": True
    }
    embed: "types.Embed" = {
        "type": "rich",
        "title": "Config AssignableRoles",
        "description": "How to configure everything concerning AssignableRoles",
        "color": embed_color(),
        "timestamp": discord_dt_string(datetime(2025, 8, 22, 23, 37, tzinfo=dt.UTC)),
        "footer": {
            "text": "Help"
        },
        "fields": [
            add_assignable_role,
            remove_assignable_role,
            set_log_channel
        ]
    }
    return Embed.from_dict(embed)
