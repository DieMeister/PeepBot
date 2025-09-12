from .data import _get_data


__all__ = [
    "bot_dt_format",
    "bot_date_format",
    "discord_dt_format"
]


def bot_dt_format() -> str:
    """Return the bot's string representation format for datetime objects."""
    return _get_data()["datetime_formats"]["datetime"]


def bot_date_format() -> str:
    """Return the bot's string representation format for date objects."""
    return _get_data()["datetime_formats"]["date"]


def discord_dt_format() -> str:
    """Return discord's string representation format for datetime objects."""
    return _get_data()["datetime_formats"]["discord"]
