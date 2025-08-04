from .checks import *
from .date_time import *
from .json_data import *
from . import getter as get
from . import sql

get.config = load_data("./config.json")
