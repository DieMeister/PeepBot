"""A package to gather all discord embed blueprints."""
from . import help
from .logs import *
from .ranks import *


__all__ = [
    "help",
    "role_log",
    "channel_log",
    "rank",
    "leaderboard"
]
