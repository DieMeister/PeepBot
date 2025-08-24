from typing import Optional


__all__ = [
    "load_data"
]


def load_data(file_path: str) -> Optional[str]:
    try:
        with open(file_path) as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return None