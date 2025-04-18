import datetime
from datetime import datetime as dt

from typing import TYPE_CHECKING
from colorama import Fore
import json

from errors import InappropriateValueError

if TYPE_CHECKING:
    import discord


data: dict
embeds: dict


def has_property(provided_properties: list[int], member_properties: list["discord.Role"]) -> bool:
    """Check if a user has a property from a provided list."""
    for i in provided_properties:
        for j in member_properties:
            if i == j.id:
                return True
    return False


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
    raw_data = json.dumps(variable, indent=4)
    with open(file_path, "w") as file:
        file.write(raw_data)


def logging(log_type: str, log_module: str, event_description: str, log_data: dict) -> None:
    """Log an event to the console and a json file.

    Positional arguments:

    ================= ============================== =======================================================================
    Argument          Description                    Additional Information
    ----------------- ------------------------------ -----------------------------------------------------------------------
    log_type          the importance of the event    must be one of the following: "info", "warning", "fatal", "debug"
    log_module        the module this event is from  must be one of the following: "bot", "twchcmds"
    event_description short description of the event can be any string
    log_data          additional information         if no additional information is provided it must be an empty dictionary
    ================= ============================== =======================================================================

    Exceptions:
    InappropriateValueError -- when an argument value is not valid (see above)
    """
    # gets the current time and creates strings for its use cases
    timestamp = dt.now(datetime.UTC)
    console_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%S")
    date = timestamp.strftime("%Y-%m-%d")

    types = {
        "info": Fore.LIGHTWHITE_EX,
        "warning": Fore.YELLOW,
        "fatal": Fore.RED,
        "debug": Fore.BLUE
    }
    modules = [
        "bot",
        "twchcmds"
    ]

    # checks if provided arguments are valid and adds them to the json file
    if log_type not in types:
        raise InappropriateValueError("Provided LoggingType does not exist")
    else:
        color = types[log_type]
        log_data["type"] = log_type

    if log_module not in modules:
        raise InappropriateValueError("Provided LoggingModule does not exist")
    else:
        log_data["module"] = log_module

    # adds additional information
    log_data["timestamp"] = file_timestamp
    log_data["event_description"] = event_description

    # saves the log entry to a json file
    file = load_data(f"Logs/{date}.json")
    if file is None:
        file = []
    file.append(log_data)
    save_data(file, f"Logs/{date}.json")

    # prints a less detailed version of the log entry to the console
    print(f"{color}[{console_timestamp}] [{log_type.upper():8}] [{log_module:8}] {event_description}{Fore.RESET}")
