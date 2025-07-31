import datetime
from datetime import datetime as dt

import lib


def get_datetime_object(datetime_string: str) -> dt:
    return dt.strptime(datetime_string, lib.get.datetime_format()).replace(tzinfo=datetime.UTC)


def get_datetime_string(datetime_object: dt) -> str:
    return datetime_object.strftime(lib.get.datetime_format())
