# TODO SHOULD NO BE USED ANYMORE

from typing import TypedDict, Optional


__all__ = [
    "Footer",
    "Image",
    "Thumbnail",
    "Author",
    "Field",
    "Embed"
]


class Footer(TypedDict):
    """A blueprint for discord EmbedFooters in json format.

    This is only for type checking.

    Attributes
    -----------
    text: Optional[:class:`str`]
        The footer text.
        Can only be up to 2048 characters.
    icon_url: Optional[:class:`str`]
        The url of the footer icon.
    """
    text: Optional[str]
    icon_url: Optional[str]


class Image(TypedDict):
    """A blueprint for discord EmbedImages in json format.

    This is only for type checking.

    Attributes
    -----------
    url: :class:`str`
        The url of the image.
    """
    url: str


class Thumbnail(TypedDict):
    """A blueprint for a discord EmbedThumbnail in json format.

    This is only for type checking.

    Attributes
    -----------
    url: :class:`str`
        The url of the Thumbnail.
    """
    url: str


class Author(TypedDict):
    """A blueprint for a discord EmbedAuthor in json format.

    This is only for type checking.

    Attributes
    -----------
    name: :class:`str`
        The name of the author of the embed.
        Can only be up to 256 characters.
    url: Optional[:class:`str`]
        The url for the author.
    icon_url: Optional[:class:`str`]
        The url of the icon of the author.
    """
    name: Optional[str]
    url: Optional[str]
    icon_url: Optional[str]


class Field(TypedDict):
    """A blueprint for a discord EmbedField in json format.

    This is only for type checking.

    Attributes
    -----------
    name: :class:`str`
        The name of the field.
        Can only be up to 256 characters.
    value: :class:`str`
        The content of the field.
        Can only be up to 1024 characters.
    inline: :class:`bool`
        Indicates if other fields can be in the same row.
    """
    name: str
    value: str
    inline: bool


class Embed(TypedDict):
    """A blueprint for discord Embeds from dictionaries.

    This is only for type checking.

    Attributes
    -----------
    title: Optional[:class:`str`]
        The title of the embed.
        Can only be up to 256 characters.
    type: :class:`str`
        Always "rich".
    description: Optional[:class:`str`]
        The description of the embed.
        Can only be up to 4096 characters.
    url: Optional[:class:`str`]
        The url of the embed.
    timestamp: Optional[:class:`str`]
        The timestamp of the embed.
        Must be a datetime string of the format "%Y-%m-%dT%H:%M:%S.%f%z"
    color: Optional[:class:`int`]
        The color code of the embed.
    footer: Optional[:class:`Footer`]
        The footer of the embed.
    image: Optional[:class:`Image`]
        The image of the embed.
    thumbnail: Optional[:class:`Thumbnail`]
        The thumbnail of the embed.
    author: Optional[:class:`Author`]
        The author of the embed.
    fields: Optional[:class:`list`[:class:`Field`]]
        The fields of the embed.
        Can only be up to 25 fields.
    """
    title: Optional[str]
    type: str
    description: Optional[str]
    url: Optional[str]
    timestamp: Optional[str]
    color: Optional[int]
    footer: Optional[Footer]
    image: Optional[Image]
    thumbnail: Optional[Thumbnail]
    author: Optional[Author]
    fields: Optional[list[Field]]
