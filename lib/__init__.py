from .checks import is_developer
from .date_time import get_datetime_string, get_datetime_object
from .json_data import load_data, save_data
from . import getter as get

get.config = load_data("./config.json")