import datetime
from datetime import datetime as dt

import logic


def get_datetime_object(datetime_string: str) -> dt:
    return dt.strptime(datetime_string, logic.config["datetime_formats"]["datetime"]).replace(tzinfo=datetime.UTC)


def get_datetime_string(datetime_object: dt) -> str:
    return datetime_object.strftime(logic.config["datetime_formats"]["datetime"])
