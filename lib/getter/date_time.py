import datetime as dt
from datetime import datetime

from lib.getter import config as get

__all__ = [
    "dt_object",
    "dt_string",
    "discord_dt_string"
]


def dt_object(datetime_string: str) -> dt:
    return datetime.strptime(datetime_string, get.dt_format()).replace(tzinfo=dt.UTC)


def dt_string(datetime_object: datetime) -> str:
    return datetime_object.strftime(get.dt_format())

def discord_dt_string(datetime_object: datetime):
    return datetime_object.strftime(get.discord_dt_format())
