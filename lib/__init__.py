from lib.json_data import *
from lib import getter as get
from lib import embeds as embed
from lib import logging
from lib import sql


__all__ =  [
    "get",
    "embed",
    "logging",
    "sql",
    "load_data",
    "save_data"
]


get.config.data = load_data("./config.json")
