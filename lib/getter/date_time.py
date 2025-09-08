import datetime as dt
from datetime import datetime

from lib.getter import config as get

__all__ = [
    "dt_object",
    "dt_string",
    "discord_dt_string",
    "now"
]


def dt_object(datetime_string: str) -> dt:
    """
    Return a datetime object from a string.

    Parameters
    -----------
    datetime_string: :class:`str`
        The datetime in string representation.
    """
    return datetime.strptime(datetime_string, get.dt_format()).replace(tzinfo=dt.UTC)


def dt_string(datetime_object: datetime) -> str:
    """
    Return a datatime object in the string format the bot uses.

    Parameters
    -----------
    datetime_object: :class:`dt`
        The datetime object to convert.
    """
    return datetime_object.strftime(get.dt_format())


def discord_dt_string(datetime_object: datetime):
    """
    Return a datetime object in the string format discord uses.

    Parameters
    -----------
    datetime_object: :class:`dt`
        The datetime object to convert.
    """
    return datetime_object.strftime(get.discord_dt_format())


def now() -> datetime:
    """Return an aware datetime object of the current time."""
    return datetime.now(dt.UTC)
