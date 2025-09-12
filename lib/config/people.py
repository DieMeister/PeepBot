from typing import TYPE_CHECKING
from .data import _get_data

if TYPE_CHECKING:
    from lib.types import Thief


__all__ = [
    "developer",
    "vip",
    "vup",
    "thieves"
]


def developer() -> list[int]:
    """Return the discord ids of the developers."""
    return _get_data()["people"]["developer"]


def vip() -> list[int]:
    """Return the discord ids of the very important people."""
    return _get_data()["people"]["vip"]


def vup() -> list[int]:
    """Return the discord ids of the very unimportant people."""
    return _get_data()["people"]["vup"]

def thieves() -> list["Thief"]:
    """Return the discord ids of the thieves."""
    return _get_data()["people"]["thieves"]
