import lib


def is_developer(user_id: int):
    """Check if a member is a developer of the Bot."""
    if user_id in lib.get.developer():
        return True
    return False
