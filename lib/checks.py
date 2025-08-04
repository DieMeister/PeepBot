from .getter import developer


__all__ = [
    "is_developer"
]


def is_developer(user_id: int) -> bool:
    """Check if a member is a developer of the Bot."""
    if user_id in developer():
        return True
    return False
