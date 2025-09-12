from typing import Union


__all__ = [
    "possible_discord_id"
]


def possible_discord_id(discord_id: Union[str, int]) -> bool:
    """Return whether something could be a discord id.

    Parameters
    -----------
    discord_id: :class:`str`
        the role id that is being checked
    """
    try:
        discord_id = int(discord_id)
    except ValueError:
        pass
    else:
        if discord_id > 10000000000000000:  # 10^16
            return True
    return False
