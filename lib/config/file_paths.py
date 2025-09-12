from .data import _get_data


__all__ = [
    "data_db_path",
    "log_db_path",
    "data_db_backup_path",
    "data_db_query_path",
    "log_db_query_path"
]


def data_db_path() -> str:
    """Return the filepath of the bot's database."""
    return _get_data()["file_paths"]["databases"]["data"]


def log_db_path() -> str:
    """Return the filepath of the bot's logging database."""
    return _get_data()["file_paths"]["databases"]["log"]


def data_db_backup_path() -> str:
    """Return the filepath of the folder to save database backups."""
    return _get_data()["file_paths"]["backups"]["data_db"]


def data_db_query_path() -> str:
    """Return the query to create the bot's database."""
    return _get_data()["file_paths"]["sql_queries"]["table_creation"]["data"]


def log_db_query_path() -> str:
    """Return the sql query to create the bot's logging database."""
    return _get_data()["file_paths"]["sql_queries"]["table_creation"]["log"]
