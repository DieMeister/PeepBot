from typing import TypedDict, Optional


__all__ = [
    "Field",
    "Footer",
    "Embed"
]

class Field(TypedDict):
    name: str
    value: str
    inline: bool


class Footer(TypedDict):
    text: str


class Embed(TypedDict):
    type: str
    title: str
    description: Optional[str]
    color: int
    timestamp: str
    footer: Footer
    fields: Optional[list[Field]]
