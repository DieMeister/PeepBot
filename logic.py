import datetime
from datetime import datetime as dt

from colorama import Fore
from lib import json_data


config: dict

def is_developer(user_id: int):
    """Check if a member is a developer of the Bot."""
    if user_id in config["people"]["developer"]:
        return True
    return False


def logging(log_type: str, log_module: str, event_description: str, log_data: dict) -> None:
    """Log an event to the console and a json file.

    Parameters
    ---------
    log_type : {'info', 'warn', 'error', 'fatal', 'debug'}
        the importance of the event
    log_module : {'bot'}
        the module that called the function
    event_description
        short description of the event
    log_data : dict
        additional information - should contain "command"; this can be a dictionary, or false if it is not a command.

        if it is a command, "command" should contain "user", "channel", "guild" and "type"

        "type" can be one of the following: "DeveloperCommand", "ManagerCommand", "UserCommand"

    Raises
    ------
    ValueError
        when an argument value is not valid (see above)
    """
    # gets the current time and creates strings for its use cases
    timestamp = dt.now(datetime.UTC)
    console_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = timestamp.strftime(config["datetime_formats"]["datetime"])
    date = timestamp.strftime(config["datetime_formats"]["date"])

    types = {
        "info": Fore.LIGHTWHITE_EX,
        "warn": Fore.MAGENTA,
        "error": Fore.YELLOW,
        "fatal": Fore.RED,
        "debug": Fore.BLUE
    }
    modules = ["bot", "peep", "config", "eastregg"]

    # checks if provided arguments are valid and adds them to the json file
    if log_type not in types:
        raise ValueError("Provided LoggingType does not exist")
    else:
        color = types[log_type]
        log_data["type"] = log_type

    if log_module not in modules:
        raise ValueError("Provided LoggingModule does not exist")
    else:
        log_data["module"] = log_module

    # adds additional information
    log_data["timestamp"] = file_timestamp
    log_data["event_description"] = event_description

    # saves the log entry to a json file
    file = json_data.load_data(f"{config['file_paths']['log_saves']}{date}.json")
    if file is None:
        file = []
    file.append(log_data)
    json_data.save_data(file, f"{config['file_paths']['log_saves']}{date}.json")

    # prints a less detailed version of the log entry to the console
    print(f"{color}[{console_timestamp}] [{log_type.upper():5}] [{log_module:8}] {event_description}{Fore.RESET}")
