import json
import os


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