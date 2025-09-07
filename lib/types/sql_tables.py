from typing import Optional


__all__ = [
    "User",
    "Guild",
    "Member"
]


type User = tuple[int, Optional[int]]
type Guild = tuple[int, str, str, str, str, int]
type Member = tuple[int, int, str, int, int, int ,int]
