"""A package to log all events connected to the PeepBot"""
from lib.logging.base import *
from lib.logging.config import *
from lib.logging.events import *
from lib.logging.extension import *
from lib.logging.moderation import *
from lib.logging.other import *
from lib.logging.peep import *


__all__ = [
    "default_logger",
    "command",
    "command_possible",
    "configure_channel",
    "change_of_assignable_roles",
    "set_log_channel",
    "change_peep_message",
    "user_join",
    "guild_join",
    "member_join",
    "extension_success",
    "extension_error",
    "assigning_role",
    "sync_commands",
    "help_embed",
    "invalid_input",
    "catch_peep",
    "psps_denied",
    "steal_peep",
    "peep_transfer",
    "rank",
    "give_peeps",
    "remove_peeps"
]
