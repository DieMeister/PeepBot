from typing import Optional, Union
import json


__all__ = [
    "load_file",
    "load_json"
]


def load_file(file_path: str) -> Optional[str]:
    """Load the content of a file as a string. Return None if the file does not exist.

    Parameters
    -----------
    file_path: :class:`str`
        The relative or absolute path to the file.
    """
    try:
        with open(file_path) as f:
            content = f.read()
    except FileNotFoundError:
        return None
    else:
        return content


def load_json(file_path: str) -> Optional[Union[dict, list]]:
    """Load a json file and return it; return None if the file does not exist.

    Parameters
    -----------
    file_path: :class:`str`
        The relative or absolute path to the file.
    """
    try:
        with open(file_path) as f:
            raw_data = f.read()
        output = json.loads(raw_data)
    except FileNotFoundError:
        output = None

    return output
