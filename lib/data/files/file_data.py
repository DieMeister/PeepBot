from typing import Optional


__all__ = [
    "load_data"
]


def load_data(file_path: str) -> Optional[str]:
    """Load the content of a file as a string. Return None if the file does not exist."""
    try:
        with open(file_path) as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return None