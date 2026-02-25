"""A package to gather all discord embed blueprints."""
from lib.embeds.logs import *
from lib.embeds.ranks import *
from lib.embeds import help


__all__ = [
    "role_log",
    "channel_log",
    "rank",
    "leaderboard",
    "help"
]
