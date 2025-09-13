from typing import TYPE_CHECKING, Optional

from lib.utils import load_json

if TYPE_CHECKING:
    from lib.types import ConfigFile, EmoteName, EmoteMarkdown


__all__ = [
    "_get_data",
    "version",
    "embed_color",
    "emote"
]


_data: Optional["ConfigFile"] = None


def _get_data() -> "ConfigFile":
    global _data
    if _data is None:
        load_json("./config.json")  # TODO check if file path is correct
    return _data


def version() -> str:
    """Return the version the bot is currently running on."""
    return _get_data()["version"]


def embed_color() -> int:
    """Return the bot's embed color code."""
    return _get_data()["embed_color"]


def emote(name: "EmoteName") -> "EmoteMarkdown":
    """Return the markdown of a provided emote name."""
    return _get_data()["emotes"][name]
