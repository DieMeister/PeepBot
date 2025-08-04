import datetime
from datetime import datetime as dt

from . import getter as get

__all__ = [
    "get_datetime_string",
    "get_datetime_object"
]


def get_datetime_object(datetime_string: str) -> dt:
    return dt.strptime(datetime_string, get.datetime_format()).replace(tzinfo=datetime.UTC)


def get_datetime_string(datetime_object: dt) -> str:
    return datetime_object.strftime(get.datetime_format())
