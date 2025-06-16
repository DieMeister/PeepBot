import json
from colorama import Fore
from typing import TYPE_CHECKING
import os

import datetime
from datetime import datetime as dt

if TYPE_CHECKING:
    import discord


database_path = "./data.json"
log_saves_directory_path = "./Logs"
data: dict


def is_developer(user_id: int):
    """Check if a member is a developer of the Bot."""
    if user_id in data["bot"]["developer"]:
        return True
    return False


def has_property(provided_properties: list[int], member_properties: list["discord.Role"]) -> bool:
    """Check if a member has a property from a provided list."""
    for i in provided_properties:
        for j in member_properties:
            if i == j.id:
                return True
    return False


def get_item(lst: list[dict], key: str, value: str | int) -> dict | None:
    """Get a specific dictionary from a list of dictionaries."""
    for i in lst:
        if key not in i:
            continue
        if i[key] == value:
            return i
    return None


def load_data(file_path: str) -> dict | list | None:
    """Load a json file and return it; return None if the file does not exist."""
    try:
        with open(file_path) as f:
            raw_data = f.read()
        output = json.loads(raw_data)
    except FileNotFoundError:
        output = None

    return output


def save_data(variable: dict | list, file_path: str) -> None:
    """Save a list or dictionary to a json file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    raw_data = json.dumps(variable, indent=2)
    with open(file_path, "w") as file:
        file.write(raw_data)


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
    file_timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%S")
    date = timestamp.strftime("%Y-%m-%d")

    types = {
        "info": Fore.LIGHTWHITE_EX,
        "warn": Fore.MAGENTA,
        "error": Fore.YELLOW,
        "fatal": Fore.RED,
        "debug": Fore.BLUE
    }
    modules = ["bot"]

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
    file = load_data(f"{log_saves_directory_path}/{date}.json")
    if file is None:
        file = []
    file.append(log_data)
    save_data(file, f"{log_saves_directory_path}/{date}.json")

    # prints a less detailed version of the log entry to the console
    print(f"{color}[{console_timestamp}] [{log_type.upper():5}] [{log_module:8}] {event_description}{Fore.RESET}")
