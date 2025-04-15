import datetime
from datetime import datetime as dt

from colorama import Fore

from errors import LoggingTypeError, LoggingModuleError


def log(log_type: str, module: str, message: str) -> None:
    timestamp = dt.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S")

    types = {
        "info": {
            "color": Fore.LIGHTWHITE_EX,
            "value": "INFO"
        },
        "warning": {
            "color": Fore.YELLOW,
            "value": "WARNING"
        },
        "fatal": {
            "color": Fore.RED,
            "value": "FATAL"
        },
        "debug": {
            "color": Fore.BLUE,
            "value": "DEBUG"
        }
    }
    modules = [
        "main",
        "bot",
        "logic"
    ]

    if module not in modules:
        raise LoggingModuleError("Provided LogModule doesn't exist")
    elif log_type not in types:
        raise LoggingTypeError("Provided LogType doesn't exist")
    else:
        color = types[log_type]["color"]
        value = types[log_type]["value"]

        print(f"{color}[{timestamp}] [{value:8}] [{module:8}] {message}{Fore.LIGHTWHITE_EX}")
