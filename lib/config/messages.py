from .data import _get_data


__all__ = [
    "log_channel_missing_msg"
]


def log_channel_missing_msg() -> str:
    """Return the message to send when a guild's logging channel is missing."""
    return _get_data()["messages"]["log_channel_missing"]
