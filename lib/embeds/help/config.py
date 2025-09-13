import datetime as dt
from datetime import datetime

from typing import TYPE_CHECKING
import discord

from lib import config
from lib.getter import discord_dt_string

if TYPE_CHECKING:
    from discord.types.embed import Embed, EmbedField, EmbedFooter


__all__ = [
    "config_peep",
    "config_assignable_role"
]


def config_peep() -> discord.Embed:
    """Return a discord embed that contains information about how to configure the peep part of the bot."""
    add_psps_channel: "EmbedField" = {
        "name": "/add_psps_channel <channel>",
        "value": "Adds a channel where `!psps` can be executed\n`channel`: The channel that is being added",
        "inline": True
    }
    remove_psps_channel: "EmbedField" = {
        "name": "/remove_psps_channel <channel>",
        "value": "Removes a channel where `!psps` can be executed.\n`channel`: The channel !psps can no longer be executed in",
        "inline": True
    }
    change_psps_message: "EmbedField" = {
        "name": "/change_psps_message <message_type> <message>",
        "value": "Changes the message that is sent after `!psps` is executed\n`message_type`: The message which's content is being changed\n`message`: The new content of the message",
        "inline": True
    }
    footer: "EmbedFooter" = {
            "text": "Help"
        }

    embed: "Embed" = {
        "type": "rich",
        "title": "Config Peep",
        "description": "How to configure everything concerning Peeps",
        "color": config.embed_color(),
        "timestamp": discord_dt_string(datetime(2025, 8, 22, 23, 37, tzinfo=dt.UTC)),
        "footer": footer,
        "fields": [
            add_psps_channel,
            remove_psps_channel,
            change_psps_message
        ]
    }
    return discord.Embed.from_dict(embed)


def config_assignable_role() -> discord.Embed:
    """Return a discord embed that contains information about how to configure the assignable role part of the bot."""
    add_assignable_role: "EmbedField" = {
        "name": "/add_assignable_role <role> [reason]",
        "value": "Adds a role to the list of roles that can be assigned using `/add_role`\n`role`: the role that is being added\n`reason`: Optional - The reason why the role is being added",
        "inline": True
    }
    remove_assignable_role: "EmbedField" = {
        "name": "/remove_assignable_role <role> [reason]",
        "value": "Removes a role from the list of roles that can be assigned using `/add_role`\n`role`: The role that is being removed\n`reason`: Optional - The reason why the role is being removed",
        "inline": True
    }
    set_log_channel: "EmbedField" = {
        "name": "/set_log_channel <channel>",
        "value": "Sets the provided channel as the channel where the bot sends logs\n`channel`: The channel logs are being sent to",
        "inline": True
    }
    footer: "EmbedFooter" = {
            "text": "Help"
        }
    embed: "Embed" = {
        "type": "rich",
        "title": "Config AssignableRoles",
        "description": "How to configure everything concerning AssignableRoles",
        "color": config.embed_color(),
        "timestamp": discord_dt_string(datetime(2025, 8, 22, 23, 37, tzinfo=dt.UTC)),
        "footer": footer,
        "fields": [
            add_assignable_role,
            remove_assignable_role,
            set_log_channel
        ]
    }
    return discord.Embed.from_dict(embed)
